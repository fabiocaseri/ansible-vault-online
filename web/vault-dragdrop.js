(function () {
  var sourceEl = document.getElementById('source');
  sourceEl.addEventListener('dragenter', onDragEnter, false);
  sourceEl.addEventListener('dragover', onDragOver, false);
  sourceEl.addEventListener('dragleave', onDragLeave, false);
  sourceEl.addEventListener('drop', onDrop, false);

  function onDragEnter(e) {
    e.stopPropagation();
    e.preventDefault();
    sourceEl.classList.add('highlight');
    return false;
  }
  function onDragOver(e) {
    e.stopPropagation();
    e.preventDefault();
    sourceEl.classList.add('highlight');
    e.dataTransfer.dropEffect = 'copy';
    return false;
  }
  function onDragLeave(e) {
    e.stopPropagation();
    e.preventDefault();
    sourceEl.classList.remove('highlight');
    return false;
  }
  function onDrop(e) {
    e.stopPropagation();
    e.preventDefault();
    sourceEl.classList.remove('highlight');

    var files = e.target.files || e.dataTransfer.files;
    if (files.length > 1) {
      return alert('Drag only one file');
    }
    handleFile(files[0]);
  }
  function handleFile(file) {
    if (/\.(yml|txt)$/.test(file.name)) {
      readTextFile(file);
    } else {
      alert('Invalid file type (only .yml and .txt accepted)');
    }
  }
  function readTextFile(file) {
    var reader = new FileReader();
    reader.onload = function () {
      sourceEl.value = reader.result;
      angular.element(sourceEl).triggerHandler('input');
    };
    reader.readAsText(file);
  }
})();
