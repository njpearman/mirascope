from unittest.mock import Mock, patch

import pytest

from mirascope.core import BaseMessageParam
from mirascope.core.base import AudioPart, ImagePart, TextPart
from mirascope.core.base._utils._convert_messages_to_message_params import (
    _convert_message_sequence_part_to_content_part,
    _convert_message_sequence_to_content,
    _is_base_message_params,
    convert_messages_to_message_params,
)


def test_convert_message_sequence_part_to_content_part_with_string():
    input_value = "Hello, World!"
    expected_output = TextPart(text="Hello, World!", type="text")
    result = _convert_message_sequence_part_to_content_part(input_value)
    assert result == expected_output


def test_convert_message_sequence_part_to_content_part_with_text_part():
    input_value = TextPart(type="text", text="Hello, World!")
    result = _convert_message_sequence_part_to_content_part(input_value)
    assert result == input_value


def test_convert_message_sequence_part_to_content_part_with_image_part():
    input_value = ImagePart(
        type="image",
        media_type="image/png",
        image=b"image_bytes",
        detail=None,
    )
    result = _convert_message_sequence_part_to_content_part(input_value)
    assert result == input_value


def test_convert_message_sequence_part_to_content_part_with_audio_part():
    input_value = AudioPart(
        type="audio",
        media_type="audio/wav",
        audio=b"audio_bytes",
    )
    result = _convert_message_sequence_part_to_content_part(input_value)
    assert result == input_value


def test_convert_message_sequence_part_to_content_part_with_pil_image():
    mock_image_instance = Mock()
    mock_image_instance.tobytes.return_value = b"image_bytes"

    from PIL import Image

    with (
        patch(
            "mirascope.core.base._utils._convert_messages_to_message_params.has_pil_module",
            True,
        ),
        patch(
            "mirascope.core.base._utils._convert_messages_to_message_params.Image.Image",
            Mock,
        ),
        patch(
            "mirascope.core.base._utils._convert_messages_to_message_params.get_image_type",
            return_value="png",
        ),
        patch(
            "mirascope.core.base._utils._convert_messages_to_message_params.isinstance",
            side_effect=lambda obj, cls: True
            if cls == Image.Image
            else isinstance(obj, cls),
        ),
    ):
        result = _convert_message_sequence_part_to_content_part(mock_image_instance)
        expected_output = ImagePart(
            type="image",
            media_type="image/png",
            image=b"image_bytes",
            detail=None,
        )
        assert result == expected_output


def test_convert_message_sequence_part_to_content_part_invalid_type():
    input_value = 12345
    with pytest.raises(ValueError) as exc_info:
        _convert_message_sequence_part_to_content_part(input_value)  # pyright: ignore [reportArgumentType]
    assert f"Invalid message sequence type: {input_value}" in str(exc_info.value)


def test_convert_message_sequence_to_content():
    input_sequence = [
        "Hello",
        TextPart(type="text", text="World"),
        ImagePart(
            type="image",
            media_type="image/jpeg",
            image=b"image_bytes",
            detail=None,
        ),
        AudioPart(
            type="audio",
            media_type="audio/mp3",
            audio=b"audio_bytes",
        ),
    ]
    expected_output = [
        TextPart(type="text", text="Hello"),
        TextPart(type="text", text="World"),
        ImagePart(
            type="image",
            media_type="image/jpeg",
            image=b"image_bytes",
            detail=None,
        ),
        AudioPart(
            type="audio",
            media_type="audio/mp3",
            audio=b"audio_bytes",
        ),
    ]
    result = _convert_message_sequence_to_content(input_sequence)
    assert result == expected_output


def test_is_base_message_params_with_base_message_param_list():
    input_value = [
        BaseMessageParam(role="user", content="Hello"),
        BaseMessageParam(role="assistant", content="Hi there!"),
    ]
    result = _is_base_message_params(input_value)
    assert result is True


def test_is_base_message_params_with_invalid_list():
    input_value = ["Hello", "World"]
    result = _is_base_message_params(input_value)
    assert result is False


def test_convert_messages_to_message_params_with_string():
    messages = "Hello, World!"
    result = convert_messages_to_message_params(messages)
    expected_output = [BaseMessageParam(role="user", content="Hello, World!")]
    assert result == expected_output


def test_convert_messages_to_message_params_with_base_message_param():
    message_param = BaseMessageParam(role="user", content="Hello")
    result = convert_messages_to_message_params(message_param)
    assert result == [message_param]


def test_convert_messages_to_message_params_with_base_message_param_list():
    messages = [
        BaseMessageParam(role="user", content="Hello"),
        BaseMessageParam(role="assistant", content="Hi!"),
    ]
    result = convert_messages_to_message_params(messages)
    assert result == messages


def test_convert_messages_to_message_params_with_sequence():
    messages = ["Hello", "World"]

    expected_output = [
        BaseMessageParam(
            role="user",
            content=[
                TextPart(type="text", text="Hello"),
                TextPart(type="text", text="World"),
            ],
        )
    ]
    result = convert_messages_to_message_params(messages)
    assert result == expected_output


def test_convert_messages_to_message_params_with_invalid_type():
    messages = 12345
    with pytest.raises(ValueError) as exc_info:
        convert_messages_to_message_params(messages)  # pyright: ignore [reportArgumentType]
    assert f"Invalid messages type: {messages}" in str(exc_info.value)


def test_convert_messages_to_message_params_with_custom_role():
    messages = "Hello, World!"
    result = convert_messages_to_message_params(messages, role="custom_role")
    expected_output = [BaseMessageParam(role="custom_role", content="Hello, World!")]
    assert result == expected_output
