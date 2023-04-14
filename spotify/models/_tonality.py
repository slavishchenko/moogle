class Tonality:
    """
    Tonality of the song.

    Spotify's audio_analysis response provides numeric values for the key and the mode of the song.
    This class maps integers to the keys, assigns mode to the key and returns tonic (chord) of the song.
    E.g Am. You can access it as 'tonality' attribute of the AudioAnalysis class.


    :ivar key: represented by an integer.
                Integers map to pitches using standard Pitch Class notation.
                E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on.
                If no key was detected, the value is -1.
                >= -1 <= 11

    :ivar key_confidence: from 0.0 to 1.0, represents the reliability of the key.
                           >= 0 <= 1

    :ivar mode: Indicates the modality (major or minor) of a track,
                 the type of scale from which its melodic content is derived.
                 Major is represented by 1 and minor is 0.

    :ivar mode_confidence: from 0.0 to 1.0, of the reliability of the mode.
                            >= 0 <= 1
    """

    KEYS_MAP = (
        (0, "C"),
        (1, "C#/Db"),
        (2, "D"),
        (3, "D#/Eb"),
        (4, "E"),
        (5, "F"),
        (6, "F#/Gb"),
        (7, "G"),
        (8, "G#/Ab"),
        (9, "A"),
        (10, "A#/Bb"),
        (11, "B"),
    )

    def __init__(
        self, key: int, key_confidence: float, mode: int, mode_confidence: float
    ) -> None:
        self.key = key
        self.key_confidence = key_confidence
        self.mode = mode
        self.mode_confidence = mode_confidence

    @staticmethod
    def assign_mode_to_the_key(key: str, mode: int) -> str:
        """Returns major or minor chord"""
        if not isinstance(key, str):
            raise TypeError("Key has to be a string")
        if not isinstance(mode, int):
            raise TypeError("Mode has to be an integer (0, 1)")
        if not mode in range(0, 2):
            raise Exception("Mode has to be either 0 or 1")

        if mode == 0:
            if not "/" in key:
                return f"{key}m"
            return "/".join([f"{k}m" for k in key.split("/")])
        return key

    @property
    def chord(self) -> str:
        """
        Returns the tonic of the song
        E.G. Am
        """
        for option in self.KEYS_MAP:
            if self.key == option[0]:
                return self.assign_mode_to_the_key(option[1], self.mode)

    @property
    def confidence(self) -> float:
        """Tonality confidence"""
        return (self.key_confidence + self.mode_confidence) / 2

    def __str__(self):
        return f"{self.chord}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.chord})"
