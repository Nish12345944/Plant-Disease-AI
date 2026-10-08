/**
 * File Validation Utility for Alexa Farms Multimodal App
 */

const SUPPORTED_IMAGE_EXTS = ['.jpg', '.jpeg', '.png', '.webp', '.bmp'];
const SUPPORTED_VIDEO_EXTS = ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.m4v'];
const SUPPORTED_AUDIO_EXTS = ['.wav', '.mp3', '.m4a', '.flac', '.ogg', '.opus', '.aac', '.webm'];

const MAX_IMAGE_SIZE_BYTES = 25 * 1024 * 1024; // 25 MB
const MAX_VIDEO_SIZE_BYTES = 100 * 1024 * 1024; // 100 MB
const MAX_AUDIO_SIZE_BYTES = 25 * 1024 * 1024; // 25 MB

export function validateMediaFile(file) {
  if (!file) {
    return { valid: false, error: 'No file provided.' };
  }

  if (file.size === 0) {
    return { valid: false, error: 'The selected file is empty (0 bytes).' };
  }

  const name = file.name || '';
  const ext = ('.' + name.split('.').pop()).toLowerCase();
  const mime = (file.type || '').toLowerCase();

  // 1. Check Image
  const isImageExt = SUPPORTED_IMAGE_EXTS.includes(ext);
  const isImageMime = mime.startsWith('image/');
  if (isImageExt || isImageMime) {
    if (file.size > MAX_IMAGE_SIZE_BYTES) {
      return {
        valid: false,
        type: 'image',
        error: `Image size exceeds the 25 MB limit (${(file.size / (1024 * 1024)).toFixed(1)} MB).`,
      };
    }
    return { valid: true, type: 'image', ext };
  }

  // 2. Check Video
  const isVideoExt = SUPPORTED_VIDEO_EXTS.includes(ext);
  const isVideoMime = mime.startsWith('video/');
  if (isVideoExt || isVideoMime) {
    if (file.size > MAX_VIDEO_SIZE_BYTES) {
      return {
        valid: false,
        type: 'video',
        error: `Video size exceeds the 100 MB limit (${(file.size / (1024 * 1024)).toFixed(1)} MB).`,
      };
    }
    return { valid: true, type: 'video', ext };
  }

  // 3. Check Audio
  const isAudioExt = SUPPORTED_AUDIO_EXTS.includes(ext);
  const isAudioMime = mime.startsWith('audio/');
  if (isAudioExt || isAudioMime) {
    if (file.size > MAX_AUDIO_SIZE_BYTES) {
      return {
        valid: false,
        type: 'audio',
        error: `Audio size exceeds the 25 MB limit (${(file.size / (1024 * 1024)).toFixed(1)} MB).`,
      };
    }
    return { valid: true, type: 'audio', ext };
  }

  return {
    valid: false,
    error: `Unsupported file format '${ext || mime || 'unknown'}'. Please upload a valid plant image (JPG, PNG, WebP) or video (MP4, WebM, MOV).`,
  };
}
