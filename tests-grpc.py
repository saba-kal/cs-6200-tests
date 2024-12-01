import subprocess
import filecmp
import os.path

# Run the server seperately:
# ./bin/dfs-server-p1 -m ./mnt/server/
# ./bin/dfs-server-p2 -m ./mnt/server/

# Configure test variables here:
client_program = "dfs-client-p2"
client_mount = "/root/projects/pr4/mnt/client/"
server_mount = "/root/projects/pr4/mnt/server/"
print_client_output = False

test_files = ["big-bear.jpg", "test-file.html"]


def main():
    test_store()
    test_list()
    test_stat()
    test_fetch()
    test_delete()
    print("\n")


def test_store():
    print("\n======= STORE FILE NOT FOUND TEST =======")
    test_store_not_found()
    print("\n======= STORE DEADLINE TEST =======")
    test_store_deadline_exceeded()
    print("\n======= STORE OK TEST =======")
    test_store_ok()


def test_list():
    print("\n======= LIST DEADLINE TEST =======")
    test_list_deadline_exceeded()
    print("\n======= LIST OK TEST =======")
    test_list_ok()


def test_stat():
    print("\n======= STAT FILE NOT FOUND TEST =======")
    test_stat_not_found()
    print("\n======= STAT DEADLINE TEST =======")
    test_stat_deadline_exceeded()
    print("\n======= STAT OK TEST =======")
    test_stat_ok()


def test_fetch():
    print("\n======= FETCH FILE NOT FOUND TEST =======")
    test_fetch_not_found()
    print("\n======= FETCH DEADLINE TEST =======")
    test_fetch_deadline_exceeded()
    print("\n======= FETCH OK TEST =======")
    test_fetch_ok()


def test_delete():
    print("\n======= DELETE FILE NOT FOUND TEST =======")
    test_delete_not_found()
    print("\n======= DELETE DEADLINE TEST =======")
    test_delete_deadline_exceeded()
    print("\n======= DELETE OK TEST =======")
    test_delete_ok()


def test_store_not_found():
    output = run_client("not_real.txt", "store")
    # No easy way to test this besides checking console output
    if "file not found" in output.lower():
        print("Store not found test: SUCCESS")
    else:
        print("Store not found test: FAIL")


def test_store_deadline_exceeded():
    output = run_client(test_files[0], "store", 1)
    if "deadline exceeded" in output.lower():
        print("Store deadline test: SUCCESS")
    else:
        print("Store deadline test: FAIL")


def test_store_ok():
    for file in test_files:
        run_client(file, "store")
        # Check that the server files are identical to client files.
        if filecmp.cmp(server_mount + file, client_mount + file, shallow=False):
            print("Store " + file + ": SUCCESS")
        else:
            print("Store " + file + ": FAIL")


def test_list_deadline_exceeded():
    output = run_client_list(1)
    if "deadline exceeded" in output.lower():
        print("List deadline test: SUCCESS")
    else:
        print("List deadline test: FAIL")


def test_list_ok():
    output = run_client_list()
    for file in test_files:
        if file in output:
            print("List " + file + ": SUCCESS")
        else:
            print("List " + file + ": FAIL")


def test_fetch_deadline_exceeded():
    output = run_client(test_files[0], "fetch", 1)
    if "deadline exceeded" in output.lower():
        print("Fetch deadline test: SUCCESS")
    else:
        print("Fetch deadline test: FAIL")


def test_stat_not_found():
    output = run_client("not_real.txt", "stat")
    if "file not found" in output.lower():
        print("Stat not found test: SUCCESS")
    else:
        print("Stat not found test: FAIL")


def test_stat_deadline_exceeded():
    output = run_client(test_files[0], "stat", 1)
    if "deadline exceeded" in output.lower():
        print("Stat deadline test: SUCCESS")
    else:
        print("Stat deadline test: FAIL")


def test_stat_ok():
    for file in test_files:
        output = run_client(file, "stat")
        # Not sure how exactly I should test this. Just print the results
        print(output)


def test_fetch_not_found():
    output = run_client("not_real.txt", "fetch")
    if "file not found" in output.lower():
        print("Fetch not found test: SUCCESS")
    else:
        print("Fetch not found test: FAIL")


def test_fetch_deadline_exceeded():
    output = run_client(test_files[0], "fetch", 1)
    if "deadline exceeded" in output.lower():
        print("Fetch deadline test: SUCCESS")
    else:
        print("Fetch deadline test: FAIL")


def test_fetch_ok():
    for file in test_files:
        run_client(file, "fetch")
        # Check that the download files are identical to server files.
        if filecmp.cmp(server_mount + file, client_mount + file, shallow=False):
            print("Fetch " + file + ": SUCCESS")
        else:
            print("Fetch " + file + ": FAIL")


def test_delete_not_found():
    output = run_client("not_real.txt", "delete")
    if "file not found" in output.lower():
        print("Delete not found test: SUCCESS")
    else:
        print("Delete not found test: FAIL")


def test_delete_deadline_exceeded():
    output = run_client(test_files[0], "delete", 1)
    if "deadline exceeded" in output.lower():
        print("Delete deadline test: SUCCESS")
    else:
        print("Delete deadline test: FAIL")


def test_delete_ok():
    for file in test_files:
        run_client(file, "delete")
        if (os.path.isfile(server_mount + file)):
            print("Delete " + file + ": FAIL")
        else:
            print("Delete " + file + ": SUCCESS")


def run_client(file, command, deadline=9000):
    args = ["./bin/" + client_program, "-m", client_mount, command, file, "-t", str(deadline)]
    result = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = str(result.stdout.read().decode())
    if print_client_output:
        print(output)
    return output


def run_client_list(deadline=9000):
    args = ["./bin/" + client_program, "-m", client_mount, "list", "-t", str(deadline)]
    result = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = str(result.stdout.read().decode())
    print(output)
    return output


if __name__ == "__main__":
    main()