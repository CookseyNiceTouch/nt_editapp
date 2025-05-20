import logging
from resolve_api import ResolveAPI

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main():
    logger.info('Testing ResolveAPI connection and project listing...')
    try:
        api = ResolveAPI()
        projects = api.list_projects()
        print('Projects:', projects)
    except Exception as e:
        logger.error('Test failed: %s', e)

if __name__ == '__main__':
    main() 