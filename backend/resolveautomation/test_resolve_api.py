import logging
import os # For path joining
import json # For pretty printing the dict
from resolve_api import ResolveAPI

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main():
    logger.info('Testing ResolveAPI functions...')
    try:
        api = ResolveAPI()
        while True:
            print("\nSelect an option:")
            print("1. List Resolve Projects")
            print("2. Create Resolve Project & Timeline")
            print("3. Get Media Pool Item Unique ID")
            print("4. Build Timeline from Edited Output JSON")
            print("5. Export Timeline as AAF")
            print("6. Exit")
            choice = input("Enter your choice (1-6): ")

            if choice == '1':
                projects = api.list_projects()
                print('Resolve Projects:')
                if projects:
                    for project_name in projects:
                        print(f"  - {project_name}")
                else:
                    print("  No projects found or error listing projects.")
            elif choice == '2':
                project_name_input = input("Enter name for new Resolve project: ")
                timeline_name_input = input("Enter name for timeline (default: Timeline 1): ") or "Timeline 1"
                project_obj = api.create_project(project_name_input)
                if project_obj:
                    print(f"Resolve Project '{project_name_input}' created.")
                    timeline_obj = api.create_timeline(project_obj, timeline_name_input)
                    if timeline_obj:
                        print(f"Timeline '{timeline_name_input}' created in project '{project_name_input}'.")
                    else:
                        print(f"Failed to create timeline '{timeline_name_input}'.")
                else:
                    print(f"Failed to create Resolve project '{project_name_input}'.")
            elif choice == '3':
                default_json_filename = "82e06fc0-ebc4-4b67-944c-aefdb6fbb3ee.json"
                json_file_name_input = input(f"Enter Nice Touch JSON filename (default: {default_json_filename}): ") or default_json_filename
                nt_json_path = os.path.join("data", json_file_name_input)
                
                default_clip_name = "20250509_MTC_2206.MP4"
                target_clip_input = input(f"Enter target clip name (default: {default_clip_name}): ") or default_clip_name
                
                print(f"Attempting to find Unique ID for clip '{target_clip_input}' using project details from '{nt_json_path}'")
                item_unique_id = api.get_media_pool_item_unique_id(nt_json_path, target_clip_input)
                
                if item_unique_id:
                    print(f"\n>>> Media Pool Item Unique ID for '{target_clip_input}': {item_unique_id} <<<")
                    print(f"   (You can use this for the 'mediapool_item_uuid' in your JSON file)")
                else:
                    print(f"Could not retrieve Unique ID for clip '{target_clip_input}'. Clip not found or error occurred. Check logs.")
            elif choice == '4':
                default_json_path = os.path.join("backend", "editgenerator", "edited_output.json")
                json_path_input = input(f"Enter path to edited output JSON (default: {default_json_path}): ") or default_json_path
                
                if not os.path.isabs(json_path_input):
                    json_path_input = os.path.abspath(json_path_input)

                default_timeline_name_build = "Nice Touch Timeline"
                timeline_name_param = input(f"Enter target timeline name (default: {default_timeline_name_build}): ") or default_timeline_name_build

                print(f"Attempting to build timeline '{timeline_name_param}' using '{json_path_input}'...")
                result = api.build_timeline_from_edited_output(json_path_input, timeline_name_param)

                if result is True:
                    print(f"Successfully built/updated timeline '{timeline_name_param}' from '{json_path_input}'. Check Resolve and logs.")
                elif result is False:
                    print(f"Failed to build/update timeline '{timeline_name_param}' using '{json_path_input}'. Check logs for details.")
                else:
                    # Should not happen if API returns bool as per new logic
                    print(f"Unexpected result from API: {result}. Check logs.")
            elif choice == '5':
                default_timeline_name = "Nice Touch Timeline"
                timeline_name_input = input(f"Enter timeline name to export (default: {default_timeline_name}): ") or default_timeline_name
                default_output_dir = os.path.join("data", "exports")
                output_dir_input = input(f"Enter output directory (default: {default_output_dir}): ") or default_output_dir

                print(f"Attempting to export timeline '{timeline_name_input}' as AAF to '{output_dir_input}'...")
                export_result = api.export_timeline_as_aaf(timeline_name_input, output_dir_input)

                if export_result and isinstance(export_result, str): # Returns filepath on success
                    print(f"Successfully exported timeline '{timeline_name_input}' to '{export_result}'")
                else:
                    print(f"Failed to export timeline '{timeline_name_input}'. Check logs for details.")
            elif choice == '6':
                print("Exiting.")
                break
            else:
                print("Invalid choice. Please try again.")
    except Exception as e:
        logger.error('Test script encountered an error: %s', e, exc_info=True)

if __name__ == '__main__':
    main() 