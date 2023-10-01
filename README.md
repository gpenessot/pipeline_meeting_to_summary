# pipeline_meeting_to_summary // UNDER CONSTRUCTION

The aim of this pipeline is to help you increase your productivity by focusing on coding while attending a (quite always) boring conference.
The steps are :
1. Record your meeting
2. Use the pipeline to sum it up into a text format
3. Use saved time to enjoy life

# Work done
- Extract audio track from a meeting recording
- Split audio track on silence to keep all words, optimize audio chunks size to run LLM on CPU
- Extract text from audio chunks
- Add punctuation to extracted text from audio chunk
- Summarize each text chunks with a relevant model

# TODO
- Merging summaries
- Data pipeline to automate the process
