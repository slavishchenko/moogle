from time import gmtime, strftime

from ._tonality import Tonality


class AudioAnalysis:
    """
    Audio Analysis model.
    Return value of the client.get_audio_analysis method.

    :ivar duration: Length of the track in seconds.
    :ivar num_samples: The exact number of audio samples analyzed form this track.
    :ivar sample_md5: This field will always contain the empty string.
    :ivar offset_seconds: An offset to the start of the region of the track that was analyzed.
                           (As the entire track is analyzed, this should always be 0.)
    :ivar window_seconds: The length of the region of the track was analyzed, if a subset of the track was analyzed.
                           (As the entire track is analyzed, this should always be 0.)
    :ivar analysis_sample_rate: The sample rate used to decode and analyze this track.
                                 May differ from the actual sample rate of this track available on Spotify.
    :ivar analysis_channels: The number of channels used for analysis.
                              If 1, all channels are summed together to mono before analysis.
    :ivar end_of_fade_in: The time, in seconds, at which the track's fade-in period ends.
                           If the track has no fade-in, this will be 0.0.
    :ivar start_of_the_fade_out: The time, in seconds, at which the track's fade-out period starts.
                                  If the track has no fade-out, this should match the track's length.
    :ivar loudnes: The overall loudness of a track in decibels (dB).
    :ivar tempo: The overall estimated tempo of a track in beats per minute (BPM).
    :ivar tempo_confidence: The confidence, from 0.0 to 1.0, of the reliability of the tempo.
    :ivar time_signature: An estimated time signature.
    :ivar time_signature_confidence: The confidence, from 0.0 to 1.0, of the reliability of the time_signature.
    :ivar key: The key the track is in.
    :ivar key_confidence: The confidence, from 0.0 to 1.0, of the reliablity of the key.
    :ivar mode: Mode indicates the modality (major or minor) of a track. Major is represented by 1 and minor is 0.
    :ivar mode_confidence: The confidence, from 0.0 to 1.0, of the reliability of the mode.
    :ivar codestring: An Echo Nest Musical Fingerprint (ENMFP) codestring for this track.
    :ivar code_version: A version number for the Echo Nest Musical Fingerprint format used in the codestring field.
    :ivar echoprintstring: An EchoPrint codestring for this track.
    :ivar exchoprint_version: A version number for the EchoPrint format used in the echoprintstring field.
    :ivar synchstring: A Synchstring for this track.
    :ivar synch_version: A version number for the Synchstring used in the synchstring field.
    :ivar rhythmstring: A Rhythmstring for this track. The format of this string is similar to the Synchstring.
    :ivar rhythm_version: A version number for the Rhythmstring used in the rhythmstring field.
    """

    def __init__(
        self,
        duration: float,
        num_samples: int,
        sample_md5: str,
        offset_seconds: int,
        window_seconds: int,
        analysis_sample_rate: int,
        analysis_channels: int,
        end_of_fade_in: float,
        start_of_fade_out: float,
        loudness: float,
        tempo: float,
        tempo_confidence: float,
        time_signature: int,
        time_signature_confidence: float,
        key: int,
        key_confidence: float,
        mode: int,
        mode_confidence: float,
        codestring: str,
        code_version: float,
        echoprintstring: str,
        echoprint_version: float,
        synchstring: str,
        synch_version: float,
        rhythmstring: str,
        rhythm_version: float,
    ) -> None:
        self.duration = duration
        self.num_samples = num_samples
        self.sample_md5 = sample_md5
        self.offset_seconds = offset_seconds
        self.window_seconds = window_seconds
        self.analysis_sample_rate = analysis_sample_rate
        self.analysis_channels = analysis_channels
        self.end_of_fade_in = end_of_fade_in
        self.start_of_fade_out = start_of_fade_out
        self.loudness = loudness
        self.tempo = tempo
        self.tempo_confidence = tempo_confidence
        self.time_signature = time_signature
        self.time_signature_confidence = time_signature_confidence
        self.key = key
        self.key_confidence = key_confidence
        self.mode = mode
        self.mode_confidence = mode_confidence
        self.codestring = codestring
        self.code_version = code_version
        self.echoprintstring = echoprintstring
        self.echoprint_version = echoprint_version
        self.synchstring = synchstring
        self.synch_version = synch_version
        self.rhythmstring = rhythmstring
        self.rhythm_version = rhythm_version

    @property
    def tonality(self):
        """Retruns the tonic of the song"""
        return Tonality(
            key=self.key,
            key_confidence=self.key_confidence,
            mode=self.mode,
            mode_confidence=self.mode_confidence,
        )

    @property
    def length(self):
        "Track length in minutes"
        return strftime("%#M.%S", gmtime(self.duration))
