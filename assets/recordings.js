(() => {
  const years = [...document.querySelectorAll('.recording-year')];
  const recordings = [...document.querySelectorAll('.recording-item')];
  const filters = [...document.querySelectorAll('.tag-filter')];
  const toggleAll = document.getElementById('toggle-all-years');
  const count = document.getElementById('recording-count');

  function closeRecording(recording) {
    recording.querySelector('audio').pause();
    recording.open = false;
  }

  function updateYearControl() {
    const visibleYears = years.filter(year => !year.hidden);
    const allClosed = visibleYears.every(year => !year.open);
    toggleAll.textContent = allClosed ? 'Expand all years' : 'Collapse all years';
    toggleAll.setAttribute('aria-expanded', String(!allClosed));
  }

  recordings.forEach(recording => {
    const audio = recording.querySelector('audio');
    const error = recording.querySelector('.audio-error');
    recording.addEventListener('toggle', () => {
      if (recording.open) {
        recordings.forEach(other => {
          if (other !== recording && other.open) closeRecording(other);
        });
      } else {
        audio.pause();
      }
    });
    audio.addEventListener('play', () => {
      recordings.forEach(other => {
        if (other !== recording) other.querySelector('audio').pause();
      });
    });
    // Source errors do not bubble to <audio> in every browser.
    audio.addEventListener('error', () => { error.hidden = false; });
    audio.querySelector('source').addEventListener('error', () => { error.hidden = false; });
    audio.addEventListener('canplay', () => { error.hidden = true; });
  });

  years.forEach(year => {
    year.addEventListener('toggle', () => {
      if (!year.open) year.querySelectorAll('.recording-item').forEach(closeRecording);
      updateYearControl();
    });
  });

  toggleAll.addEventListener('click', () => {
    const visibleYears = years.filter(year => !year.hidden);
    const shouldOpen = visibleYears.every(year => !year.open);
    visibleYears.forEach(year => {
      year.open = shouldOpen;
      if (!shouldOpen) year.querySelectorAll('.recording-item').forEach(closeRecording);
    });
    updateYearControl();
  });

  filters.forEach(filter => {
    filter.addEventListener('click', () => {
      const selected = filter.dataset.tag;
      filters.forEach(button => button.setAttribute('aria-pressed', String(button === filter)));
      let visibleCount = 0;
      recordings.forEach(recording => {
        const matches = selected === 'all' || JSON.parse(recording.dataset.tags).includes(selected);
        recording.hidden = !matches;
        if (matches) visibleCount += 1;
        else closeRecording(recording);
      });
      years.forEach(year => {
        const visible = [...year.querySelectorAll('.recording-item')].filter(recording => !recording.hidden);
        year.hidden = visible.length === 0;
        year.querySelector('.year-count').textContent = `${visible.length} recording${visible.length === 1 ? '' : 's'}`;
      });
      count.textContent = `${visibleCount} recording${visibleCount === 1 ? '' : 's'}`;
      updateYearControl();
    });
  });
})();
