import os

import dropbox
from decouple import config
from tqdm import tqdm


def upload(
        access_token,
        file_path,
        target_path,
        timeout=900,
        chunk_size=4 * 1024 * 1024,
):
    dbx = dropbox.Dropbox(access_token, timeout=timeout)
    with open(file_path, "rb") as f:
        file_size = os.path.getsize(file_path)
        if file_size <= chunk_size:
            print(dbx.files_upload(f.read(), target_path))
        else:
            with tqdm(total=file_size, desc="Uploaded") as pbar:
                upload_session_start_result = dbx.files_upload_session_start(
                    f.read(chunk_size)
                )
                pbar.update(chunk_size)
                cursor = dropbox.files.UploadSessionCursor(
                    session_id=upload_session_start_result.session_id,
                    offset=f.tell(),
                )
                commit = dropbox.files.CommitInfo(path=target_path)
                while f.tell() < file_size:
                    if (file_size - f.tell()) <= chunk_size:
                        print(
                            dbx.files_upload_session_finish(
                                f.read(chunk_size), cursor, commit
                            )
                        )
                    else:
                        dbx.files_upload_session_append(
                            f.read(chunk_size),
                            cursor.session_id,
                            cursor.offset,
                        )
                        cursor.offset = f.tell()
                    pbar.update(chunk_size)


if __name__ == '__main__':
    FILENAMES = ('doc2vec.model4', 'doc2vec.model4.dv.vectors.npy',
                 'doc2vec.model4.wv.vectors.npy', 'doc2vec.model4.syn1neg.npy')

    DROP_BOX_PASS = config('DROP_BOX')
    dbx = dropbox.Dropbox(DROP_BOX_PASS, timeout=90_000)

    # for filename in FILENAMES:
    #     print(f'Uploading {filename}')
    #     with open(f'models/{filename}', 'rb') as f:
    #         dbx.files_upload(f.read(), f'/{filename}')
    print('Uploading large')
    upload(DROP_BOX_PASS, 'models/doc2vec.model4.syn1neg.npy', '/doc2vec.model4.syn1neg.npy', 9000)
    print('done')
