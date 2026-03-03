export default function isJdLinkOrDescription(text: string): boolean {
  const urlRegex = /^(https?:\/\/)?([\w-]+\.)+[\w-]+(\/[\w\-._~:/?#[\]@!$&'()*+,;=]*)?$/i;
  return urlRegex.test(text.trim());
}
