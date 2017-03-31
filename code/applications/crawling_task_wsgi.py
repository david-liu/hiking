from crawling_task_service import app, initialize_app
from hiking.utils import helper

initialize_app(helper.convert_to_abspath(__file__, 'APP.INI'), 'crawling_task')

if __name__ == "__main__":
    app.run()