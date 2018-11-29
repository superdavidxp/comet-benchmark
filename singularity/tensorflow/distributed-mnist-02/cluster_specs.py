from more_itertools import unique_everseen
import argparse

FLAGS=None


def main():
    f = open(FLAGS.hosts_file,'r')
    hosts_list = []
    for line in f:
        hosts_list.append(line.strip())
    f.close()
    hosts_list = list(unique_everseen(hosts_list))

    # print("|    hosts_list = {}".format(hosts_list))

    # all hosts other than ps are all treated as workers, comet-XX-XX is for comets, for other clusters, you may change correspondingly
    ps_hosts = [hosts_list[i] + ".sdsc.edu:2222" for i in range(FLAGS.num_ps_hosts)]
    worker_hosts = [hosts_list[i] + ".sdsc.edu:2222" for i in range(len(ps_hosts), len(hosts_list))]
    
    # print("|    ps_hosts = {}".format(ps_hosts))
    # print("|    worker_hosts = {}".format(worker_hosts))

    print(','.join(ps_hosts), ','.join(worker_hosts))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.register("type", "bool", lambda v: v.lower() == "true")
    parser.add_argument(
        "--hosts_file",
        type=str,
        default=""
        )
    parser.add_argument(
    	"--num_ps_hosts",
    	type=int,
    	default=1
    	)
    
    FLAGS, unparsed = parser.parse_known_args()

    main()
