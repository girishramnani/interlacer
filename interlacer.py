import argparse
import itertools
import logging as lg
import os
import subprocess

lg.basicConfig(format='%(levelname)s:%(message)s ', level=lg.DEBUG)


def test_ffmpeg():
    exit_code, output = subprocess.getstatusoutput("ffmpeg")
    if exit_code != 1:
        lg.error("ffmpeg is not installed on our system")
    else:
        lg.debug("ffmpeg is installed..")


def mkdir(directory):
    os.mkdir(directory)  # we dont care if it fails.


def parse_args(args):

    parser = argparse.ArgumentParser(prog="interlacer",
                                     description="""Interlace two videos into one cronologically
                                            and alternating for use with active 3d movies""")
    
    parser.add_argument(
        "-in", type=str, help='Input folders (should be two)', nargs="+")
    parser.add_argument("-out", type=str, required=True)
    return parser.parse_args(args)


def rename_folders(folder, name_gen, pressesion=6):
    files = os.listdir(folder)
    extname = os.path.splitext(files[0])[1]
    for old_name, new_name in zip(sorted(files), name_gen):
        lg.info("renaming {} to {}".format(old_name, new_name))
        os.rename("{}/{}".format(folder, old_name),
                  "{}/{:07d}{}".format(folder, new_name, extname))


def generate_images(inp, out, frate=30, formt="jpg"):
    mkdir(out)
    args = '-y -r {} -i "{}" -qscale 0 "{}/image.%06d.{}"'.format(
        frate, inp, out, formt)
    lg.debug("Generating the images at {}".format(out))
    _, output = subprocess.getstatusoutput("ffmpeg {}".format(args))
    lg.info(output)



def move_all(infol1,infol2,outfol):
    pass 


def create_video(inf, outfile):
    command = """ffmpeg -start_number 0 -i "{}/%7d.jpg" -c:v libx264 -vf "fps=25,format=yuv420p"  {}"""
    _, output = subprocess.getstatusoutput(command.format(inf,outfile))
    lg.debug(output)

odd = lambda: itertools.count(1, 2)
even = lambda: itertools.count(0, 2)

if __name__ == "__main__":
    test_ffmpeg()
    generate_images("1.mp4","output3")
    generate_images("2.mp4","output4")
    rename_folders("output3",odd())
    rename_folders("output4",even())
