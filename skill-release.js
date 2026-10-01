// 2026-10-01: all catalog skills are open. The earlier weekly batch is retired.
(function (root) {
  const START = '2026-10-01';

  function releasedCount(total) {
    return total;
  }
  function isReleased(n, total, now) {
    return n >= 1 && n <= releasedCount(total, now);
  }
  function nextDate() {
    return null;
  }
  function formatDate(d) {
    if (!d) return '';
    const parts = new Intl.DateTimeFormat('zh-CN', {
      timeZone: 'Asia/Shanghai',
      month: 'numeric',
      day: 'numeric'
    }).formatToParts(d);
    const month = (parts.find(p => p.type === 'month') || {}).value;
    const day = (parts.find(p => p.type === 'day') || {}).value;
    return month + '月' + day + '日';
  }

  function readerNote() {
    return '';
  }

  root.SKILL_RELEASE = {
    start: START,
    batchSize: 0,
    initial: null,
    releasedCount: releasedCount,
    isReleased: isReleased,
    nextDate: nextDate,
    formatDate: formatDate,
    readerNote: readerNote,
    filter: function (skills, now) {
      const limit = releasedCount(skills.length, now);
      return skills.filter(s => s.n <= limit);
    }
  };
})(window);
