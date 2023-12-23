# noqa: D100

class BetamaxError(Exception):  # noqa: D101
    def __init__(self, message):  # noqa: D107
        super(BetamaxError, self).__init__(message)


class MissingDirectoryError(BetamaxError):  # noqa: D101
    pass


class ValidationError(BetamaxError):  # noqa: D101
    pass


class InvalidOption(ValidationError):  # noqa: D101
    pass


class BodyBytesValidationError(ValidationError):  # noqa: D101
    pass


class MatchersValidationError(ValidationError):  # noqa: D101
    pass


class RecordValidationError(ValidationError):  # noqa: D101
    pass


class RecordIntervalValidationError(ValidationError):  # noqa: D101
    pass


class PlaceholdersValidationError(ValidationError):  # noqa: D101
    pass


class PlaybackRepeatsValidationError(ValidationError):  # noqa: D101
    pass


class SerializerValidationError(ValidationError):  # noqa: D101
    pass


validation_error_map = {
    'allow_playback_repeats': PlaybackRepeatsValidationError,
    'match_requests_on': MatchersValidationError,
    'record': RecordValidationError,
    'placeholders': PlaceholdersValidationError,
    'preserve_exact_body_bytes': BodyBytesValidationError,
    're_record_interval': RecordIntervalValidationError,
    'serialize': SerializerValidationError,  # TODO: Remove this
    'serialize_with': SerializerValidationError
}
