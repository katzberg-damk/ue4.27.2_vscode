import json
import os

def get_workspace_defs():
    c_cpp_properties_file = open(".vscode\\c_cpp_properties.json")
    data = json.load(c_cpp_properties_file)
    files=[];
    files.append(data["configurations"][0]["compileCommands"])
    files.append(data["configurations"][1]["compileCommands"])
    c_cpp_properties_file.close()
    return files
    
def find_ue4(file_path):
    file = open(file_path)
    data = json.load(file)
    file.close()
    return data[0]["directory"].replace("\\Engine\\Source", "\\.vscode").replace("\"", "")

def fix_strings(file_path):
    file = open(file_path, "r")
    data = json.load(file)
    data_copy = data.copy()
    command_to_change = data[0]["command"].split("@")[0].strip()
    command_changed = "\"" + command_to_change + "\" "
    print(command_to_change)
    print(command_changed)
    for entry_id in range(0, len(data_copy)):
        data_copy[entry_id]["command"] = data[entry_id]["command"].replace(command_to_change, command_changed)
    file.close()
    file = open(file_path, "w")
    json.dump(data_copy, file, sort_keys=False, indent=4)
    file.close()

def find_target():
    for file in os.listdir("./"):
        if file.endswith(".uproject"):
            return file

def regenerate_project_files(ue4_dir):
    target_name = find_target()
    print(target_name)
    build_bat_path = ue4_dir.replace("\\.vscode", "\\Engine\\Build\\BatchFiles\\Build.bat")
    target_path = os.getcwd() +"\\" + target_name
    build_bat_path = "\"" + build_bat_path + "\""
    print(build_bat_path + " -ProjectFiles " + target_path)
    os.system(build_bat_path + " -ProjectFiles " + target_path)

def main():
    file_paths = get_workspace_defs()
    files = []
    ue4_dir = find_ue4(file_paths[0])
    for file_path in file_paths:
        file = file_path.split("\\")
        files.append(file[-1])

    for file in files:
        file_paths.append(ue4_dir +"\\" + file);
    regenerate_project_files(ue4_dir)

    for file_path in file_paths:
        fix_strings(file_path)


if __name__ == "__main__":
    main()