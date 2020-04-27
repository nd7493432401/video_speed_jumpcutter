import os
import glob

input_file = '2_PhasePlaneAnalysis.mp4'
filename = input_file[:-4]
sec_per_part = '6bb00'
output_file = input_file[:-4]+'_SHORT.mp4'

os.system('python ffmpeg-split.py -f ' + input_file + ' -s ' + sec_per_part )

concat_files = 'concat:'
for input_part_file in sorted(glob.glob(filename + "*-of-*.mp4"), key=os.path.getmtime):
	print('--------------now: '+input_part_file)
	output_part_file = input_part_file[:-4]+'_ALT.mp4'
	output_part_file_ts = input_part_file[:-4]+'_ALT.ts'
	if (concat_files[-1] != ':'):
		concat_files += '|'
	concat_files += output_part_file_ts
	if(len(glob.glob(output_part_file))>0):
		print("----------------skipped : "+output_part_file)
		continue
	os.system('python3  jumpcutter.py --input_file ' + input_part_file + ' --output_file ' + output_part_file + ' --sounded_speed 2 --silent_speed 10 --frame_margin 2')
	os.system("ffmpeg -i "+ output_part_file + " -c copy -bsf:v h264_mp4toannexb -f mpegts " + output_part_file_ts)
	
# TODO: Combine the output files 
# for output_part_file in glob.glob("*-of-*ALTERED.mp4"):
# 	ffmpeg -i output_part_file -c copy -bsf:v h264_mp4toannexb -f mpegts intermediate1.ts
# # ffmpeg -i input2.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts intermediate2.ts
print('----------concat file :' + concat_files)
os.system("ffmpeg -i \"" + concat_files + "\" -c copy -bsf:a aac_adtstoasc " + output_file);
os.system("rm *ALT.ts")
os.system("rm *ALT.mp4")
os.system("rm *-of-*.mp4")