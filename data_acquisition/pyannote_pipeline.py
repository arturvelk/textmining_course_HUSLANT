from pyannote.audio import Pipeline
from huggingface_hub import HfApi
import concurrent.futures
import pandas as pd
from pydub import AudioSegment
import os
import time

# Get the list of all files and directories
path = "C:/Users/Velkey Artúr/Desktop/Textmining/videok/MZP/hangfileok/new files"
path_to_export = "C:/Users/Velkey Artúr/Desktop/Textmining/videok/MZP/hangfileok/trimmed_files"
mzp_file_list = [i for i in os.listdir(path) if i[:3] == "mzp"]
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@develop", use_auth_token="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")

def run_pipeline(filename):
    
    dia = pipeline(f"{path}/{filename}")
    sajt = {"start" : [],"end" : [], "speaker" : []}
    
    for speech_turn, track, speaker in dia.itertracks(yield_label = True):
        sajt["start"].append(speech_turn.start)
        sajt["speaker"].append(speaker)
        sajt["end"].append(speech_turn.end)

    speaker_identified_ = (
    pd.DataFrame(sajt).groupby(["speaker"])
    .count()
    .reset_index()
    .sort_values(by = "start", ascending = False)
    .speaker
    .to_list()[0]
    )
    
    audio_cut_list = pd.DataFrame(sajt).loc[lambda _df: _df["speaker"] == speaker_identified_,:].to_dict("r")
    sajt = AudioSegment.from_wav(f"{path}/{filename}")
    audio = sajt[audio_cut_list[0]["start"]*1000:audio_cut_list[0]["end"]*1000]
    for dikt in audio_cut_list[1:]:
        audio += sajt[dikt["start"]*1000:dikt["end"]*1000]
    audio.export(f"{path_to_export}/{filename}", format="wav")


if __name__ == "__main__":
    print("most kezdődik a futás")
    start_time = time.time() 

    with concurrent.futures.ThreadPoolExecutor(max_workers=11) as executor:
        executor.map(run_pipeline, mzp_file_list)

    total_time = time.time() - start_time

    print(total_time)