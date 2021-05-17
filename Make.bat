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
FOR /R html/data %%G IN (*input.mp4) DO (
    python .\Zeitkippen.py --input-file "%%G" --log-level DEBUG --save-frames True
)
