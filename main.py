from masker import Masker
import click

@click.command()
@click.option('-i', 'inputfile', type=click.Path(exists=True,resolve_path=True), required=True)
@click.option('-o', 'outputfolder', type=click.Path(resolve_path=True), default=None, required=False, help='Specify folder to save masked video.')
@click.option('-hsv', 'hsvparams', type=click.Path(resolve_path=True), default=None, required=False,
              help='JSON file path with HSV filter parameters. Expected format: {"hMin": 0, "sMin": 0, "vMin": 0, "hMax": 179, "sMax": 255, "vMax": 255, "sAdd": 0, "sSub": 0, "vAdd": 0, "vSub": 0, "blur": 0, "close": 0, "object": 0, "hole": 0}. Filter parameters and value ranges: MinHue (0 to 179), MinSaturation (0 to 255), MinValue (0 to 255), MaxHue (0 to 179), MaxSaturation (0 to 255), MaxValue (0 to 255), SaturationAdd (0 to 255), SaturationSubtract (0 to 255), ValueAdd (0 to 255), ValueSubtract (0 to 255), Clahe (0 or 1, switch on CLAHE application per frame before masking), Blur (0 to 10, increases kernel size), Close (0 to 10, increases kernel size), Small Object Removal (0 to 25000 in pixels), Small Hole Removal (0 to 25000 in pixels)')
@click.option('-guimode/-no-guigmode', 'guimode', default=False,
            help='Launches a GUI with two windows, one loops the input video and the other the current mask per frame. Includes trackbars for HSV filter parameters to find the appropriate mask thresholds in real time.' )

def VideoMasking(inputfile, outputfolder, hsvparams, guimode):
    # Load Video
    video = Masker(inputfile)
    
    if guimode:
        print('Initiating GUI mode. Press Q to exit...')
        video.init_video_gui()
    else:
        video.mask_and_export(outputfolder, hsvparams)

if __name__ == "__main__":

    VideoMasking()
