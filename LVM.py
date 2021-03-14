def lvm():

	while True :
		os.system("clear")
		o_p = render("LVM",colors=['red','yellow'],align='center')
		print(o_p)
		os.system('espeak-ng "WELCOME TO LVM MENU"')
		cprint("""
                                                              ================================================
                                                              | No.|           SERVICES                      |
                                                              ================================================
                                                              | 1. | To see all disks available              |
                                                              ------------------------------------------------
                                                              | 2. | To see all existing volume group        |
                                                              ------------------------------------------------
                                                              | 3. | To see  a existing volume  group        |
                                                              ------------------------------------------------
                                                              | 4. | To see  all logical volume(lv)          | 
                                                              ------------------------------------------------
                                                              | 5. | To see all partitions and mount points  |
                                                              ------------------------------------------------
                                                              | 6. | To create volume group                  |
                                                              ------------------------------------------------
                                                              | 7. | To create a lv partition                |
                                                              ------------------------------------------------
                                                              | 8. | To resize a lv partition                |
                                                              ------------------------------------------------
                                                              | 9. | To remove a virtual group               |
                                                              ------------------------------------------------
                                                              | 10.| To delete a Partition                   |
                                                              ------------------------------------------------
                                                              | 11.| To go back to main menu                 |
                                                              ------------------------------------------------
""",'yellow')
		cprint("Enter your Choice:",'yellow',end='')
		input_ = int(input())
		if input_ == 1:
			output = sp.getstatusoutput("fdisk -l")
		elif input_ == 2:
			output = sp.getstatusoutput("vgdisplay")
		elif input_ == 3:
			cprint("Enter a volume Group name to see info :",'yellow',end='')
			vg_name = input()
			output = sp.getstatusoutput("vgdisplay {}".format(vg_name))
		elif input_ == 4:
			#cprint("Enter logical volume name : ",'yellow',end='')
			#lv_name = input()
			output = sp.getstatusoutput("lvdisplay")
		elif input_ == 5:
			output = sp.getstatusoutput("df -h")
		elif input_ == 6:
			cprint("Enter volume group name : ",'yellow',end='')
			vg_name = input()
			cprint("Enter number of physical volume you want to add : ",'yellow',end='')
			num = input() 
			num = int(num)
			disks = [input("Enter disk {} name : ".format(i)) for i in range(num)]
			print("disks")
			s = " "
			s = s.join(disks)
			os.system("pvcreate {}".format(s))
			output = sp.getstatusoutput("vgcreate {} {}".format(vgname,s))
			info = sp.getstatusoutput("vgdisplay {}".format(vgname))
			print(info[1])
			output = sp.getstatusoutput("vgdisplay {}".format(vg_name))
		elif input_ == 7:
			cprint("Enter vgname in which you want to create partition : ",'yellow',end='')
			vg_name = input()
			cprint("Enter Logical volume name : ",'yellow',end='')
			lv_name = input()
			cprint("Enter size of lv [K,M,G] : ",'yellow',end='')
			size = input()
			cprint("Enter a folder path to which you want to link partition : ",'yellow',end='')
			mount_point = input()
			output = sp.getstatusoutput("lvcreate -n {} --size {} {} ".format(lv_name,size,vg_name))
			print(output[1],"\n")
			if(output[0] == 0):
				output = sp.getstatusoutput("mkfs.ext4 /dev/{}/{}".format(vg_name,lv_name))
				print(output[1],"\n") 
				if(output[0] == 0):
					os.system("mkdir {}".format(mount_point))
					output = sp.getstatusoutput("mount /dev/{}/{} {}".format(vg_name,lv_name,mount_point))
				info = sp.getstatusoutput("lvdisplay {}/{}".format(vg_name,lv_name))
				print(info[1])
		elif input_ == 8:
			cprint("Enter virtual group name in which logicl volume  partition is present : ",'yellow',end='')
			vg_name =input()
			cprint("Enter logival volume name : ",'yellow',end='')
			lv_name =input ()
			cprint("Enter 'R' to reduce and 'E' to extend size : ",'yellow',end='')
			option =input()
			cprint("Enter final size [K,M,G,T,P,E] you want to achieve after extend/reduce : ",'yellow',end='')
			size =input ()
			if option == 'R':
				mount_point = sp.getoutput("findmnt -n -o TARGET /dev/{}/{}".format(vg_name,lv_name))
				output = sp.getstatusoutput("umount /dev/{}/{}".format(vg_name,lv_name))
				print(output[1],"\n")
				if(output[0] == 0):
					x = os.system("e2fsck -f /dev/{}/{}".format(vg_name,lv_name))
					output = sp.getstatusoutput("resize2fs /dev/{}/{} {}".format(vg_name,lv_name,size))
					print(output[1],"\n")
					if(output[0] == 0):
						cprint("Enter y if you want to continue else enter n",'yellow')
						output = sp.getstatusoutput("lvreduce -L {} /dev/{}/{}".format(size,vg_name,lv_name))
						if(output[0] == 0):
							output=sp.getstatusoutput("mount /dev/{}/{} {}".format(vg_name,lv_name,mount_point))
			elif option == 'E':
				output = sp.getstatusoutput("lvextend -L {} /dev/{}/{}".format(size,vg_name,lv_name))
				if(output[0] == 0):
					output = sp.getstatusoutput("resize2fs /dev/{}/{}".format(vg_name,lv_name))
			info = sp.getstatusoutput("lvdisplay {}/{}".format(vg_name,lv_name))
			print(info[1])

		elif input_ == 9:
			cprint("Enter virtual group name which you want to delete : ",'yellow',end='')
			vg_name =input()
			output = sp.getstatusoutput("vgchange -a n {}".format(vgname))
			if(output[0] == 0):
				output = sp.getstatusoutput("vgremove {}".format(vg_name))
		elif input_ == 10:
			cprint("Enter virtual group name of which logical volume is a part : ",'yellow',end='')
			vg_name =input()
			cprint("Enter logical volume name which you wish to delete : ",'yellow',end='')
			lv_name =input()
			output = sp.getstatusoutput("umount /dev/{}/{}".format(vg_name,lv_name))
			if(output[0] == 0):
				output = sp.getstatusoutput("lvremove -y /dev/{}/{}".format(vg_name,lv_name))
		elif input_ == 11:
			break
		else:
			print("Invalid Choice ! Try Again")
			os.system("sleep 1")
			continue
		outputcheck(output)	