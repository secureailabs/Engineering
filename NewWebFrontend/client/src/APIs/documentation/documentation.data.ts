import {TGetDocumentationSuccess, TGetAllDocumentationsSuccess} from './documentation.typeDefs';
import { MdOutlineMoveToInbox, MdOutlineAssessment, MdOutlineSlowMotionVideo } from 'react-icons/md';

const getting_started: TGetDocumentationSuccess = {
  id: '323c9895-8d3e-40e8-b043-eb42819a80f2',
  icon: MdOutlineAssessment,
  primaryText: 'Getting Started',
  secondaryText: "Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
  documentationUrl: 'http://www.secureailabs.com',
}

const data_annotation_tool: TGetDocumentationSuccess = {
  id: '4923ea1d-edcc-4ffb-917b-84ea527c99b6',
  icon: MdOutlineMoveToInbox,
  primaryText: "Data Annotation Tool",
  secondaryText: "Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
  documentationUrl: 'http://www.secureailabs.com',
}

const videos: TGetDocumentationSuccess = {
  id: '323c9895-8d3e-40e8-b043-eb42819a80f2',
  icon: MdOutlineSlowMotionVideo,
  primaryText: 'Videos',
  secondaryText: "Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
  documentationUrl: 'http://www.secureailabs.com',
}

const documentations_data: TGetAllDocumentationsSuccess = {
  documentations: [
    data_annotation_tool,
    videos,
    getting_started,
  ],
};

export default documentations_data;
