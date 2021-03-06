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
XCOPY /S /E/Y doc\data html\data

@REM Process all videos named input.mp4 in subfolders off data/html.
FOR /D %%D in (html\data\*) DO (
    python .\Zeitkippen.py --input-file %%D\input.mp4 --log-level DEBUG
)