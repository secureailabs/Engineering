import {TGetDocumentationSuccess, TGetAllDocumentationSuccess} from './documentation.typeDefs';
import { MdOutlineMoveToInbox, MdOutlineAssessment, MdOutlineSlowMotionVideo } from 'react-icons/md';

const getting_started: TGetDocumentationSuccess = {
  id: "031a7d42-fdd0-4d3d-9ded-fef985bce107",
  icon: MdOutlineAssessment,
  primaryText: "Getting Started",
  secondaryText: "Overview and Tutorials on how to use the SAIL Unified Patient Registry platform.",
  documentationUrl: "http://www.secureailabs.com",
}

const data_annotation_tool: TGetDocumentationSuccess = {
  id: "4923ea1d-edcc-4ffb-917b-84ea527c99b6",
  icon: MdOutlineMoveToInbox,
  primaryText: "Data Annotation Tool",
  secondaryText: "Documentation for the Data Annotation Tool, for packaging and uploading data sets.",
  documentationUrl: "http://www.secureailabs.com",
}

const videos: TGetDocumentationSuccess = {
  id: "323c9895-8d3e-40e8-b043-eb42819a80f2",
  icon: MdOutlineSlowMotionVideo,
  primaryText: "Videos",
  secondaryText: "Overview and Tutorials on how to use the SAIL Unified Patient Registry platform.",
  documentationUrl: "http://www.secureailabs.com",
}

const documentation_data: TGetAllDocumentationSuccess = {
  documentation: [
    data_annotation_tool,
    videos,
    getting_started,
  ],
};

export default documentation_data;
