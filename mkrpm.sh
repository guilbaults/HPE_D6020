#!/bin/bash
spectool -g -R HPE_D6020-el7.spec
rpmbuild --define "dist .el7" -ba HPE_D6020-el7.spec
