'use strict';
(() => {
  const status = document.getElementById('status');
  const open = document.getElementById('open-app');
  const copy = document.getElementById('copy-code');
  const params = new URLSearchParams(location.search);
  const values = params.getAll('code');
  const value = values[0] || '';
  const valid = location.search.length <= 512 && !location.hash &&
    [...params.keys()].length === 1 && values.length === 1 &&
    /^\?code=[^&?+#]+$/.test(location.search) &&
    /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(value) &&
    value !== '00000000-0000-0000-0000-000000000000';
  if (!valid) {
    status.textContent = '초대 코드가 올바르지 않아요. 친구에게 새 링크를 부탁해 주세요.';
    return;
  }
  const code = value.toLowerCase();
  const scheme = 'panchigi://join?code=' + encodeURIComponent(code);
  document.getElementById('invite-code').textContent = code;
  open.href = scheme;
  open.setAttribute('aria-disabled', 'false');
  copy.disabled = false;
  status.textContent = '앱이 열리지 않으면 위 버튼을 눌러 주세요.';
  copy.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(code);
      copy.textContent = '복사했어요!';
    } catch (_) {
      // Local/file render and older in-app browsers may lack the clipboard API.
      const input = document.createElement('textarea');
      input.value = code; input.setAttribute('readonly', '');
      document.body.appendChild(input); input.select();
      const copied = document.execCommand('copy'); input.remove();
      copy.textContent = copied ? '복사했어요!' : '코드를 길게 눌러 복사해 주세요';
    }
  });
  // One attempt only; there is no redirect loop and no code sent to a third party.
  const timer = setTimeout(() => {
    if (document.visibilityState === 'visible') location.href = scheme;
  }, 300);
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'hidden') clearTimeout(timer);
  }, { once: true });
})();
