import { TDocumentationFailureProps } from "./Documentation.types";

const DocumentationFailure : React.FC<TDocumentationFailureProps> = () => {
  return (
    <p>There was an error fetching the list of documentation pages. Please try again later...</p>
  );
};

export default DocumentationFailure;
