import {TGetDownloadSuccess, TGetAllDownloadsSuccess} from './download.typeDefs';
import { MdOutlineMoveToInbox } from 'react-icons/md';


const data_annotation_tool: TGetDownloadSuccess = {
  id: '4923ea1d-edcc-4ffb-917b-84ea527c99b6',
  icon: MdOutlineMoveToInbox,
  primaryText: "Data Annotation Tool",
  secondaryText: "Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
  version: '0.0.1',
  publish_date: 'March 1, 2020',
  buttonText: 'Download',
  buttonUrl: 'https://sailcomputationimage9891.blob.core.windows.net/builds/SecureComputationNode.tar.gz?sp=r&st=2022-07-26T17:34:48Z&se=2023-06-02T01:34:48Z&spr=https&sv=2021-06-08&sr=b&sig=anz7KTHbjS8MEG3amKRaWiMndM0b2QwD7Wn9v%2B6TtA4%3D',
  documentationUrl: 'http://www.secureailabs.com',
  fileSize: '1.0 MB',
  systemRequirements: 'Windows 10, Chrome, Firefox, Safari',
}

const another_tool: TGetDownloadSuccess = {
  id: '323c9895-8d3e-40e8-b043-eb42819a80f2',
  icon: MdOutlineMoveToInbox,
  primaryText: 'Another Tool',
  secondaryText: "Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
  version: '0.0.1',
  publish_date: '2020-01-01',
  buttonText: 'Download',
  buttonUrl: 'string',
  documentationUrl: 'http://www.secureailabs.com',
  fileSize: '1.0 MB',
  systemRequirements: 'Windows 10, Chrome, Firefox, Safari',
}

const downloads_data: TGetAllDownloadsSuccess = {
  downloads: [
    data_annotation_tool,
    another_tool,
  ],
};

export default downloads_data;