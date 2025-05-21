import logging
from resolve_api import ResolveAPI

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main():
    logger.info('Testing ResolveAPI connection and project listing...')
    try:
        api = ResolveAPI()
        while True:
            print("\nSelect an option:")
            print("1. List Projects")
            print("2. Create Timeline in New Project")
            print("3. Exit")
            choice = input("Enter your choice (1-3): ")
            if choice == '1':
                projects = api.list_projects()
                print('Projects:')
                for project in projects:
                    print(f"  - {project}")
            elif choice == '2':
                project_name = input("Enter the name for the new project: ")
                timeline_name = input("Enter the name for the timeline (default: Timeline 1): ") or "Timeline 1"
                project = api.create_project(project_name)
                if project:
                    print(f"Project '{project_name}' created successfully.")
                    timeline = api.create_timeline(project, timeline_name)
                    if timeline:
                        print(f"Timeline '{timeline_name}' created successfully in project '{project_name}'.")
                    else:
                        print(f"Failed to create timeline '{timeline_name}'.")
                else:
                    print(f"Failed to create project '{project_name}'.")
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")
    except Exception as e:
        logger.error('Test failed: %s', e)

if __name__ == '__main__':
    main() 