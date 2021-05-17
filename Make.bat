@REM Make all precomputed data for the Zeitkippen project 
@REM This involves presenting the premade videos in the right folders,
@REM creating synthetic samples from Python code and then running the
@REM Zeitkippen tool on each of those.

@REM Remove old data and create a fresh data folder
RMDIR html\data /s /q
MKDIR html\data

@REM Create synthetic sample videos by script.
python .\BuildSampleVideos.py

@REM Prepare real-world sample videos.
MKDIR html\data\Basketball
COPY doc\Basketball.mp4 html\data\Basketball\input.mp4

@REM Process all videos named input.mp4 in subfolders off data/html.
FOR /D %%D in (html\data\*) DO (
    python .\Zeitkippen.py --input-file %%D\input.mp4 --log-level DEBUG --save-frames True
    
    ffmpeg -framerate 24 -i %%D\xy\%%04d.png -movflags faststart -pix_fmt yuv420p -an %%D\xy.mp4
    ffmpeg -framerate 24 -i %%D\xt\%%04d.png -movflags faststart -pix_fmt yuv420p -an %%D\xt.mp4
    ffmpeg -framerate 24 -i %%D\yt\%%04d.png -movflags faststart -pix_fmt yuv420p -an %%D\yt.mp4
)