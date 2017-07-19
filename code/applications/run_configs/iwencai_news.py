### -*- coding: utf-8 -*- 
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from hiking.utils import parser_helper, url_helper
from hiking.core.run_config import ByKeys, FieldTypeKeys, FieldMultiplicityKeys, RunConfig

SITE_URL = 'http://www.iwencai.com/'

keywords = [u"3D打印", u"3G", u"4D打印", u"4G", u"5G", u"APEC会议", u"BIT", u"CDM减排", u"G20峰会", u"HPV疫苗", u"IGBT", u"IPV6", u"LNG天然气", u"MERS", u"NFC", u"O2O", u"OGS触控屏", u"OLED", u"P2P", u"PM2.5", u"POCT", u"PPP", u"PTA", u"PVC", u"SAAS", u"SDR", u"SNS", u"TMT", u"WIFI", u"阿里巴巴", u"阿糖胞苷", u"埃博拉", u"癌症定量检测", u"安防", u"氨纶", u"奥运会", u"白酒", u"白糖", u"白银", u"保健品", u"保障房", u"比特币", u"殡葬", u"玻璃纤维", u"超导", u"超级电容", u"超级计算机", u"超声治疗", u"超硬材料", u"车联网", u"充电桩", u"触摸屏", u"传感器", u"创投", u"春节", u"磁悬浮", u"存准率", u"达菲", u"大飞机", u"大健康", u"大容量通信", u"大数据", u"大消费", u"单抗", u"低碳经济(CDM)", u"迪士尼", u"地热能", u"地下管网", u"电解锰", u"电缆", u"电子发票", u"电子竞技", u"电子商务", u"电子书", u"电子烟", u"电子政务", u"冬奥会", u"动漫", u"动物免疫", u"毒胶囊", u"多晶硅", u"多肽药", u"厄尔尼诺", u"儿童消费品", u"儿童用药", u"二手车", u"二胎", u"发电机", u"钒电池", u"反恐", u"防辐射", u"房地产中介", u"废品回收", u"废气处理", u"分布式发电", u"分离膜", u"分散染料", u"风电", u"风沙治理", u"服务外包", u"富勒烯", u"改革", u"干细胞", u"钢结构", u"高端装备", u"高功率光纤", u"高考", u"高岭土", u"高铁", u"高校", u"高性能膜", u"工控信息安全", u"工业4.0", u"工业互联网", u"工业节水", u"工业用地", u"公共交通", u"公路建设", u"供气", u"供应链金融", u"骨传导", u"固废处理", u"固态硬盘", u"冠状病毒", u"光伏", u"光热", u"光纤", u"轨道交通", u"海底隧道", u"海上风电", u"海水淡化", u"海峡西岸", u"海洋执法", u"航空发动机", u"航空航天", u"航空租赁", u"航母", u"航天系", u"航运", u"好莱坞", u"合成革", u"核电", u"核污染防治", u"互联网+", u"互联网保险", u"互联网彩票", u"互联网出版", u"互联网电力", u"互联网电视", u"互联网钢铁", u"互联网广告", u"互联网金融", u"互联网平台", u"互联网期货", u"互联网汽车", u"互联网券商", u"互联网医疗", u"互联网银行", u"环保包装", u"环境监测", u"黄金", u"黄金水道", u"黄金租赁", u"火箭军", u"机床制造", u"机器人", u"机器视觉", u"基因测序", u"基因疗法", u"基因芯片", u"激光器", u"集成电路", u"家禽养殖", u"家用电器", u"钾离子电池", u"检测认证", u"胶合板", u"胶原蛋白", u"焦虑症", u"节能环保", u"节水灌溉", u"结核病", u"金融IC", u"金融信息服务", u"净水器", u"军工", u"抗癌", u"抗艾滋病", u"抗辐射药", u"抗寒", u"抗旱", u"可见光通信", u"可降解塑料", u"可燃冰", u"空气净化", u"空中巴士", u"口罩", u"跨境电商", u"快递", u"宽带中国", u"狂犬病", u"垃圾发电", u"蓝宝石", u"老龄化", u"雷达", u"冷链物流", u"锂电池", u"量子霍尔", u"量子计算", u"量子通信", u"钌催化剂", u"磷化工", u"磷酸铁锂", u"螺纹钢", u"裸眼3D", u"铝材加工", u"绿色建筑", u"绿色消费", u"马歇尔计划", u"煤化工", u"煤矿安全", u"镁空气电池", u"棉纺织", u"棉花种植", u"民营金融", u"民营医院", u"膜材料", u"纳米材料", u"纳米抗擦墨", u"纳米印刷", u"奶牛养殖", u"南海", u"南水北调", u"能源互联网", u"牛羊肉", u"农村电商", u"农业现代化", u"诺贝尔", u"帕拉米韦", u"配电网", u"啤酒", u"葡萄酒", u"普洱茶", u"期货", u"气凝胶", u"汽车电商", u"汽车电子", u"铅蓄电池", u"禽流感", u"青蒿素", u"轻型合金", u"氢燃料电池", u"情人节", u"区块链", u"去IOE", u"全息手机", u"燃油", u"人工降雨", u"人工角膜", u"人工智能", u"人脸识别", u"人民币", u"人脑工程", u"人造太阳", u"融资租赁", u"柔性电子", u"乳业", u"三氯甲烷", u"三农", u"三网融合", u"奢侈品", u"涉矿", u"生态农业", u"生物农药", u"生物疫苗", u"圣诞节", u"石墨烯", u"食品安全", u"食品包装", u"食用油", u"手机芯片", u"手机游戏", u"手势识别", u"手足口病", u"数据存储", u"数字电视", u"数字货币", u"数字音乐", u"双十一", u"水产品", u"水处理膜", u"私人飞机", u"搜索引擎", u"塑化剂", u"台风", u"太阳能", u"钛白粉", u"炭疽", u"碳纳米管", u"碳纤维", u"特钢", u"特高压", u"特斯拉", u"特许经营权", u"特种玻璃", u"体感交互", u"体外诊断", u"体育产业", u"调味品", u"铁矿石", u"铁路基建", u"通信基站", u"通用航空", u"铜冶炼", u"透明计算", u"土地流转", u"土壤修复", u"脱硫脱硝", u"外贸", u"网红", u"网络安全", u"网络电视", u"网络游戏", u"危险废物治理", u"微电子", u"维稳", u"尾气治理", u"卫星导航", u"文化传媒", u"污水处理", u"无人岛开发", u"无人机", u"无人驾驶", u"无线充电", u"物联网", u"物流骨干网", u"稀缺煤", u"稀缺资源", u"稀土永磁", u"稀土整合", u"稀有金属", u"现代服务业", u"现代渔业", u"线材", u"箱板纸", u"象牙", u"橡胶", u"消防装备", u"消费金融", u"小额贷款", u"小间距led", u"小金属", u"锌电池", u"锌二氧化锰", u"新材料", u"新能源", u"虚拟现实", u"虚拟运营商", u"循环经济", u"压缩空气储能", u"烟花爆竹", u"眼动技术", u"眼科医疗", u"羊绒", u"养老", u"遥感技术", u"药店", u"页岩气", u"液态金属", u"一带一路", u"医保", u"医疗器械", u"医药电商", u"依法治国", u"仪电仪表", u"胰岛素", u"移动pos机", u"移动互联网", u"移动金融", u"移动入口", u"移动支付", u"乙肝", u"忆阻器", u"疫苗存储", u"音乐产业", u"银联", u"引力波", u"饮料包装", u"隐身技术", u"营改增", u"永磁高铁", u"油菜籽", u"油改气", u"油价", u"铀矿", u"游轮", u"有轨电车", u"有机硅", u"有机食品", u"有声读物", u"幼儿教育", u"余额宝", u"余热发电", u"羽绒服", u"语音技术", u"预警机", u"园林开发", u"阅兵", u"云计算", u"灾备存储", u"再生金属", u"在线教育", u"在线旅游", u"早籼稻", u"造纸转暖", u"增强现实", u"征信", u"知识产权", u"职业教育", u"指纹技术", u"致密气", u"智慧城市", u"智能表", u"智能穿戴", u"智能电视", u"智能电网", u"智能家居", u"智能建筑", u"智能交通", u"智能物流", u"智能眼镜", u"智能医疗", u"智能终端", u"中医药", u"众筹", u"重金属治理", u"猪肉", u"专网通信", u"转基因", u"自动售货机", u"棕榈油", u"足球", u"董事会决议", u"非公开发行", u"风险警示", u"复牌", u"股东大会", u"股权激励", u"财报", u"首次公开发行IPO", u"停牌", u"退市", u"异常波动", u"员工持股", u"增发", u"资产重组", u"违法违规"]

CSS_SELECTORS = {
    "title" :  {
        'key' : '.title_word',
        'is_primary' : True
    },
    "summary" : '.s_r_summ',
    'detail_url' : 'table h2.s_r_title > a'
}

def _list_detail_page_urls(browser):
    base_url = 'http://www.iwencai.com/search?typed=0&preParams=&ts=1&f=1&qs=result_tab&selfsectsn=&querytype=&bgid=&sdate=&edate=&searchfilter=&tid=news'

    urls = {}
    for keyword in keywords:
        url = url_helper.build_url(base_url, {'w': keyword})
        urls[keyword] = url

    return urls

def in_page_jumping_fn(browser):
    next_links =  browser.find_elements_by_css_selector(".grayr a")

    if len(next_links) == 0:
        return False

    if next_links[-1].text.strip()==u'下一页':
        next_links[-1].click();
        return True
    else:
        return False

def _datails_page_element_processor(element):
    url = parser_helper.get_element_attribute(element, 'href')
    return url

def create_run_config():
    return RunConfig(
        site_url=SITE_URL,
        field_selectors=CSS_SELECTORS,
        list_detail_page_urls_fn=_list_detail_page_urls,
        block_selector='.s_r_box',
        in_page_jumping_fn=in_page_jumping_fn,
        field_element_processors={
            'detail_url' : _datails_page_element_processor})
