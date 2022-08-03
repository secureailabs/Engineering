import {
  TGetAllDownloadsSuccess,
  TGetDownloadSuccess,
  TGetDownloadStart,
} from './download.typeDefs';

import downloads_data from './download.data';

export const getDownloadAPIDemo = async (data: TGetDownloadStart): Promise<TGetDownloadSuccess|unknown> => {
  return downloads_data.downloads.find(download => download.id === data.id) ? downloads_data.downloads.find(download => download.id === data.id) : null;
}

export const getAllDownloadsAPIDemo = async(): Promise<TGetAllDownloadsSuccess['downloads']> => {
  return downloads_data.downloads;
}
