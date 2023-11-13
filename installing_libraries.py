# The multithreading function takes as a parameter the variable libraries of the "list" type, which stores a list of
# libraries and frameworks that need to be installed. The subroutine divides the installation of libraries and
# frameworks into threads and launches them.
def multithreading(libraries: list):
    from threading import Thread
    from subprocess import run

    threads = []
    for library in range(len(libraries)):
        threads.append(Thread(target=run, args=(libraries[library],)))
        threads[library].start()
    for thread in threads:
        thread.join()


# The run_commands function takes as parameters path variables of the string type, which stores the path to the file
# with settings, libraries of the "list" type, which stores the list of libraries, frameworks that need to be
# installed, and upgrade of the boolean type, which is necessary to change console commands. The popprogram updates
# "pip", divides the resulting libraries and frameworks into 2 processes and launches the multithreading function,
# after which it records the update date of the libraries and frameworks in a file with settings.
def run_commands(path: str, libraries: list, upgrade: bool):
    from multiprocessing import Pool
    from subprocess import run
    from file_actions import set_attribute
    from datetime import datetime

    run(['pip', 'install', '--upgrade', 'pip'])
    libraries = [
        ['pip', 'install', '--upgrade', library] if upgrade else ['pip', 'install', library] for library in libraries
    ]
    libraries_size = len(libraries)
    libraries = [
        [libraries[library] for library in range(0, libraries_size // 2)],
        [libraries[library] for library in range(libraries_size // 2, libraries_size)]
    ]
    with Pool(2) as pool:
        pool.map(multithreading, libraries)
    set_attribute(
        path_to_file=path,
        name_attribute='last_update',
        new_value=f'{datetime.today().strftime("%d-%m-%Y")}'
    )


# The installing_libraries function takes as parameters path variables of the string type, which stores the path to the
# file with settings, libraries of the "list" type, which stores the libraries and frameworks that need to be installed
# for the program to work. The subroutine receives the latest update of libraries, frameworks and updates them using
# the run_commands function, if any, otherwise the program installs the necessary libraries, frameworks using the
# run_commands function.
def installing_libraries(path: str, libraries: list):
    from file_actions import get_attribute
    from datetime import datetime

    last_update = get_attribute(path_to_file=path, name_attribute='last_update')
    if last_update == '':
        run_commands(path=path, libraries=libraries, upgrade=False)
    elif abs(datetime.strptime(last_update, '%d-%m-%Y') - datetime.now()).days > 6:
        run_commands(path=path, libraries=libraries, upgrade=True)
