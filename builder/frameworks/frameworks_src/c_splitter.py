
import re
import os


def split_c_files(env, node):
    src_file_content = node.get_text_contents()

    # Splits at // <--#SPLIT#--> //
    split_src_file_content = re.split(r'^[^S\n\r]*//[^S\n\r]*<--#SPLIT#-->[^S\n\r]*//[^S\n\r]*\r?\n', src_file_content, flags=re.MULTILINE | re.IGNORECASE)
    # No split:
    if len(split_src_file_content) <= 1:
        return node

    source_file_directory = str(node.srcnode().dir)
    target_file_directory = str(node.dir)
    os.makedirs(target_file_directory, exist_ok=True)
    orig_file_name = node.name
    orig_file_name_wo_ext, orig_extension = os.path.splitext(orig_file_name)

    print(f'Splitting {orig_file_name} into:')

    part_files = []
    # The part of the file before the first split will be included in every part
    includes = split_src_file_content[0]
    for i, part in enumerate(split_src_file_content[1:]):
        part_file_name = f'{orig_file_name_wo_ext}_part_{i}{orig_extension}'
        part_file_content = f'{includes}\n{part}'
        part_file_path = os.path.join(target_file_directory, part_file_name)

        with open(part_file_path, 'w') as part_file:
            part_file.write(part_file_content)

        part_files.append(env.File(part_file_path))
        print(f'\t{part_file_name}')

    return env.Object(part_files, CPPPATH=[source_file_directory] + env['CPPPATH'])


def print_info(node):
    node_info = dir(node)
    for info_element in node_info:
        attribute = None
        call_result = None
        try:
            attribute = getattr(node, info_element)
            call_result = attribute()
        except:
            pass
        print(f'{info_element}:\n\t{attribute}\n\t{call_result}')
