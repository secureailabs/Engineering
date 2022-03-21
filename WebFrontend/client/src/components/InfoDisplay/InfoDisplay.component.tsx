import React from 'react';
import GridLayout from 'react-grid-layout';

import { TInfoDisplay } from './InfoDisplay.types';

const InfoDisplay: React.FC<TInfoDisplay> = ({ title, data }) => {
  return (
    <div className="info-display">
      {title && <div className="info-display__header">{title}</div>}
      <div className="info-display__content">
        {data.map(
          (
            {
              section_title,
              section_data,
              data_parser,
              conditional = true,
              to_locale_date_string,
              color = 'black',
            },
            index
          ) => {
            if (data_parser) {
              section_data = data_parser(section_data);
            }

            if (to_locale_date_string) {
              section_data = new Date(section_data * 1000).toLocaleDateString(
                'en-US',
                {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                }
              );
            }
            if (conditional) {
              return (
                <div key={index} className="info-display__section">
                  <div className="info-display__section__title">
                    {section_title}
                  </div>
                  <div
                    className="info-display__section__text"
                    style={{ color }}
                  >
                    {section_data}
                  </div>
                </div>
              );
            }
          }
        )}
      </div>
    </div>
  );
};

export default InfoDisplay;
