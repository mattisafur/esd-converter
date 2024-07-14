import subprocess


def dism_get_wiminfo(source_file_path: str) -> str:
    try:
        result = subprocess.run(f'dism /get-wiminfo /wimfile:{source_file_path}',
                                stdout=subprocess.PIPE, check=True)
        return result.stdout.decode()
    except subprocess.CalledProcessError as error:
        match error.returncode:
            case 2:
                raise FileNotFoundError
            case _:
                raise error


def dism_export_image(source_file_path: str, source_index: str, destination_file_path: str) -> None:
    try:
        subprocess.run(f'dism /export-image /sourceimagefile:{source_file_path} /sourceindex:{source_index} /destinationimagefile:{destination_file_path} /compress:max /checkintegrity',
                       stdout=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as error:
        match error.returncode:
            case 2:
                raise FileNotFoundError
            case _:
                raise error


def parse_dism_get_wiminfo_output(dism_get_wiminfo_output: str) -> list[dict[str, str]]:
    print(list(dism_get_wiminfo_output)) # TODO remove line

    # strip start and end of output, leaving only the image information
    start_phrase: str = 'Index : 1'
    end_phrase: str = 'bytes'

    index: int = dism_get_wiminfo_output.find(start_phrase)
    trimmed_output: str = dism_get_wiminfo_output[index:]

    index = trimmed_output.rfind(end_phrase) + len(end_phrase)
    trimmed_output = trimmed_output[:index]

    print(list(trimmed_output)) # TODO Remove line

    # split string to images
    images: list[str] = trimmed_output.split('\r\n\r\n')

    print(images) # TODO remove line

    # parse each image to a dictionary and append it to a list
    parsed_output: list[dict[str, str]] = []
    for image in images:
        parsed_image: dict[str, str] = {}
        for line in image.split('\r\n'):
            key, val = line.split(' : ')
            parsed_image[key] = val
        parsed_output.append(parsed_image)

    return parsed_output
