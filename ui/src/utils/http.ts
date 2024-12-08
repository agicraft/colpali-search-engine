export const upload = async ({
  method,
  url,
  formData,
  onProgress,
}: {
  method: string;
  url: string;
  formData: FormData;
  onProgress?: (e: ProgressEvent) => void;
}): Promise<void> => {
  return new Promise(function (resolve, reject) {
    const xhr = new XMLHttpRequest();

    const fail = () => {
      let json = null;
      try {
        json = JSON.parse(xhr.responseText);
      } catch (e) {}
      const msg = `${(json && (json.detail || json.error)) || xhr.responseText || 'Failed to upload'} (${
        xhr.status || 0
      })`;
      reject(new Error(msg));
    };

    xhr.onreadystatechange = function () {
      if (xhr.readyState != 4) {
        // done
        return;
      }
      if (xhr.status != 200) {
        fail();
        return;
      }
      resolve();
    };

    xhr.addEventListener('error', () => fail());

    if (onProgress) {
      xhr.addEventListener('progress', onProgress);
    }

    xhr.open(method, url, true);
    xhr.send(formData);
  });
};
