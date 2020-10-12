# pyATS  - Stateful Network Validation

## Overview

Originally developed for internal Cisco engineering use, pyATS is at the core of Cisco's Test Automation Solution.
https://developer.cisco.com/docs/pyats/#!introduction/cisco-pyats-network-test-automation-solution

## What does this project do?
pyATS can do a lot of things, the aim of this repo is to show how to use pyATS to perform stateful network validation.

## Example
In this example, we will show how we can use pyATS on a Nexus switch to detect a VNI going down.

### Environment
There is an existing docker container which contains everything you need to run pyATS.
https://hub.docker.com/r/ciscotestautomation/pyats

### How does this work?
As pyATS has been developed by Cisco, it can easily by used on Cisco OS (IOSXE, NXOS, IOSXR, SDWAN...), it already contains a lot of parser and
models. All we have to do is to ask pyATS to "learn" the state of a device at one moment, then we ask pyATS to do the same at a different time.
For example this can be done before and after a maintenance operation. After that, all we have to do is to make a diff.
A file written in yaml (testbed.yaml) indicated to which devices it has to interact.
https://developer.cisco.com/docs/genie-docs/

### Show us
The below command can be broken down in two parts:
- docker run -it -v /opt/scripts/pyats/:/automation ciscotestautomation/pyats:latest -> this launch the docker container
- pyats learn vxlan interface platform --testbed-file /automation/testbed.yaml --output /automation/learnt -> this is the pyats command, we will focus on this part

```
docker run -it -v /opt/scripts/pyats/:/automation ciscotestautomation/pyats:latest pyats learn vxlan interface platform --testbed-file /automation/testbed.yaml --output /automation/learnt
[Entrypoint] Starting pyATS Docker Image ...
[Entrypoint] Workspace Directory: /pyats
[Entrypoint] Activating workspace
Enter default password for device LST-DC2C-001
Password: 

Learning '['vxlan', 'interface', 'platform']' on devices '['LST-DC2C-001']'
 33%|â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–                                                                                 67%|â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–100%|â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–100%|â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–| 3/3 [01:25<00:00, 28.48s/it]
+==============================================================================+
| Genie Learn Summary for device LST-DC2C-001                                  |
+==============================================================================+
|  Connected to LST-DC2C-001                                                   |
|  -   Log: /automation/learnt/connection_LST-DC2C-001.txt                     |
|------------------------------------------------------------------------------|
|  Learnt feature 'vxlan'                                                      |
|  -  Ops structure:  /automation/learnt/vxlan_nxos_LST-DC2C-001_ops.txt       |
|  -  Device Console: /automation/learnt/vxlan_nxos_LST-DC2C-001_console.txt   |
|------------------------------------------------------------------------------|
|  Learnt feature 'interface'                                                  |
|  -  Ops structure:  /automation/learnt/interface_nxos_LST-DC2C-001_ops.txt   |
|  -  Device Console: /automation/learnt/interface_nxos_LST-                   |
| DC2C-001_console.txt                                                         |
|------------------------------------------------------------------------------|
|  Learnt feature 'platform'                                                   |
|  -  Ops structure:  /automation/learnt/platform_nxos_LST-DC2C-001_ops.txt    |
|  -  Device Console: /automation/learnt/platform_nxos_LST-DC2C-001_console.txt |
|==============================================================================|
```


In the pyATS command, we are asking to learn the vxlan and interfaces states on the device referenced in testbed.yaml and to store it under
the learnt directory.

Then, to trigger a change we will shutdown a VLAN interface (ip forward), which will bring down the VNI:
```
LST-DC2C-001(config)# int vlan 3967
LST-DC2C-001(config-if)# shutdown 
```

And then we perform the same command to learn the state after the change, but we store it in a different directory:

```
[root@pla-jmich-p01 pyats]# docker run -it -v /opt/scripts/pyats/:/automation ciscotestautomation/pyats:latest pyats learn vxlan interface --testbed-file /automation/testbed.yaml --output /automation/after
[Entrypoint] Starting pyATS Docker Image ...
[Entrypoint] Workspace Directory: /pyats
[Entrypoint] Activating workspace
Enter default password for device LST-DC2C-001
Password: 

Learning '['vxlan', 'interface']' on devices '['LST-DC2C-001']'
 50%|â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–                              100%|â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–100%|â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–| 2/2 [01:20<00:00, 40.21s/it]
+==============================================================================+
| Genie Learn Summary for device LST-DC2C-001                                  |
+==============================================================================+
|  Connected to LST-DC2C-001                                                   |
|  -   Log: /automation/after/connection_LST-DC2C-001.txt                      |
|------------------------------------------------------------------------------|
|  Learnt feature 'vxlan'                                                      |
|  -  Ops structure:  /automation/after/vxlan_nxos_LST-DC2C-001_ops.txt        |
|  -  Device Console: /automation/after/vxlan_nxos_LST-DC2C-001_console.txt    |
|------------------------------------------------------------------------------|
|  Learnt feature 'interface'                                                  |
|  -  Ops structure:  /automation/after/interface_nxos_LST-DC2C-001_ops.txt    |
|  -  Device Console: /automation/after/interface_nxos_LST-DC2C-001_console.txt |
|==============================================================================|
```

All we have to do is to check the diff between the two states:

```bash
[root@pla-jmich-p01 pyats]# docker run -it -v /opt/scripts/pyats/:/automation ciscotestautomation/pyats:latest pyats diff /automation/learnt /automation/after --output /automation/
[Entrypoint] Starting pyATS Docker Image ...
[Entrypoint] Workspace Directory: /pyats
[Entrypoint] Activating workspace
1it [00:00, 10.35it/s]
+==============================================================================+
| Genie Diff Summary between directories /automation/learnt/ and               |
| /automation/after/                                                           |
+==============================================================================+
|  File: vxlan_nxos_LST-DC2C-001_ops.txt                                       |
|   - Diff can be found at /automation/diff_vxlan_nxos_LST-DC2C-001_ops.txt    |
|------------------------------------------------------------------------------|
|  File: interface_nxos_LST-DC2C-001_ops.txt                                   |
|   - Diff can be found at /automation/diff_interface_nxos_LST-DC2C-001_ops.txt |
|------------------------------------------------------------------------------|
```

pyATS found differences, let's have a look:
```
[root@pla-jmich-p01 pyats]# cat diff/diff_vxlan_nxos_LST-DC2C-001_ops.txt 
--- /automation/learnt/vxlan_nxos_LST-DC2C-001_ops.txt
+++ /automation/after/vxlan_nxos_LST-DC2C-001_ops.txt
l2route:
 topology:
  topo_id:
-   3967: 
-    topo_name: 
-     Vxlan-400379: 
-      emulated_ip: 0.0.0.0
-      emulated_ro_ip: 0.0.0.0
-      encap_type: 1
-      flags: L3cp
-      if_hdl: 1224736769
-      iod: 0
-      prev_flags: -
-      rcvd_flag: 0
-      rmac: b4de.31f2.bd27
-      sub_flags: --
-      topo_name: Vxlan-400379
-      topo_type: vni
-      tx_id: 26
-      vmac: b4de.31f2.bd27
-      vni: 400379
-      vrf_id: 5
-      vtep_ip: 172.26.15.209
nve:
 nve1:
  vni:
   400379:
+    vni_state: down
-    vni_state: up
 vni:
  summary:
+   cp_vni_down: 1
-   cp_vni_down: 0
+   cp_vni_up: 17
-   cp_vni_up: 18
[root@pla-jmich-p01 pyats]# cat diff/diff_interface_nxos_LST-DC2C-001_ops.txt 
--- /automation/learnt/interface_nxos_LST-DC2C-001_ops.txt
+++ /automation/after/interface_nxos_LST-DC2C-001_ops.txt
info:
 Vlan3967:
+  enabled: False
-  enabled: True
+  oper_status: down
```

Pretty cool, pyATS found the VNI and the interfaces went down!

# pyATS made easier
Ok, you might think it is difficult to use cause of docker. So I developped two python scripts to make things easier.

# Requirements
You need to have docker installed for this, with of course the pyATS image installed.


## getState.py
This script will take a snapshot of a device state. All you have to do is:
 ./getState.py username deviceHostname directory models 
 
### Example:
```
[root@pla-jmich-p01 pyats]# ./getState.py t.pessione LST-DC2C-001 post interface
[Entrypoint] Starting pyATS Docker Image ...
[Entrypoint] Workspace Directory: /pyats
[Entrypoint] Activating workspace
Enter default password for device LST-DC2C-001
Password: 

Learning '['interface']' on devices '['LST-DC2C-001']'
100%|â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–100%|â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–â–| 1/1 [00:05<00:00,  5.52s/it]
+==============================================================================+
| Genie Learn Summary for device LST-DC2C-001                                  |
+==============================================================================+
|  Connected to LST-DC2C-001                                                   |
|  -   Log: /automation/res/post/connection_LST-DC2C-001.txt                   |
|------------------------------------------------------------------------------|
|  Learnt feature 'interface'                                                  |
|  -  Ops structure:  /automation/res/post/interface_nxos_LST-DC2C-001_ops.txt |
|  -  Device Console: /automation/res/post/interface_nxos_LST-                 |
| DC2C-001_console.txt                                                         |
|==============================================================================|
```

## diffState.py
This script will compare the states between two reps:
 ./diffState.py directory1 directory2 directoryToStoreResult

### Example
```
[root@pla-jmich-p01 pyats]# ./diffState.py pre post test
[Entrypoint] Starting pyATS Docker Image ...
[Entrypoint] Workspace Directory: /pyats
[Entrypoint] Activating workspace
1it [00:00, 36.32it/s]
+==============================================================================+
| Genie Diff Summary between directories /automation/res/pre/ and              |
| /automation/res/post/                                                        |
+==============================================================================+
|  File: interface_nxos_LST-DC2C-001_ops.txt                                   |
|   - Diff can be found at /automation/diff/test/diff_interface_nxos_LST-      |
| DC2C-001_ops.txt                                                             |
|------------------------------------------------------------------------------|
```
