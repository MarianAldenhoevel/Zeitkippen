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
MKDIR html\data\_Basketball
COPY doc\_Basketball.mp4 html\data\_Basketball\input.mp4

MKDIR html\data\_Eadweard_Muybridge
COPY doc\_Eadweard_Muybridge.mp4 html\data\_Eadweard_Muybridge\input.mp4

MKDIR html\data\_Space_Invaders
COPY doc\_Space_Invaders.mp4 html\data\_Space_Invaders\input.mp4

@REM Process all videos named input.mp4 in subfolders off data/html.
FOR /D %%D in (html\data\*) DO (
    python .\Zeitkippen.py --input-file %%D\input.mp4 --log-level DEBUG
)