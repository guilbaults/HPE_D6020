#!/usr/bin/python3
import HPE_D6020
import pprint
import argparse


def main():
    parser = argparse.ArgumentParser(
        description='Find the position of a block device in a HPE D6020')
    parser.add_argument('block', help='name of the block device')
    parser.add_argument('--mpath', help='handle a multipath device',
                        action='store_true')
    parser.add_argument('--alias', help='alias')
    args = parser.parse_args()

    enclosures = HPE_D6020.Enclosure().get_enclosures()

    if args.mpath:
        jbod_bay = HPE_D6020.Enclosure().jbod_multipath_bay(args.block)
    else:
        jbod_bay = HPE_D6020.Enclosure().jbod_bay(args.block)

    jbod_name = jbod_bay[0]
    bay = jbod_bay[1]

    if args.alias:
        # use the alias instead of the wwn
        jbod_name = HPE_D6020.Enclosure().jbod_alias(jbod_name, args.alias)
    print('{0}-bay{1}'.format(jbod_name, bay))


if __name__ == '__main__':
    main()
