import React, { useState } from 'react';

import Text from '@secureailabs/web-ui/components/Text';

import Measure from 'react-measure';

import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Doughnut } from 'react-chartjs-2';
import { Range, getTrackBackground } from 'react-range';

import HighlightedValue from '@secureailabs/web-ui/components/HighlightedValue';

ChartJS.register(ArcElement, Tooltip, Legend);

import Card from '@secureailabs/web-ui/components/Card';

import Select from 'react-select';
const STEP = 0.1;
const MIN = 0;
const MAX = 100;
const rtl = false;
export const gender_data = {
  labels: ['Male', 'Female', 'Unkown'],
  datasets: [
    {
      label: 'Total No. Of Patients',
      data: [114, 26, 20],
      backgroundColor: [
        'rgba(243, 115, 36, 0.8)',
        'rgba(134, 158, 166, 0.8)',
        'rgba(0, 0, 0, 0.8)',
      ],
      borderColor: [
        'rgba(243, 115, 36, 1)',
        'rgba(134, 158, 166, 1)',
        'rgba(0, 0, 0, 1)',
      ],
      borderWidth: 2,
    },
  ],
};

const plugins = [
  {
    beforeDraw: function (chart) {
      var width = chart.width,
        height = chart.height,
        ctx = chart.ctx;
      ctx.restore();
      var fontSize = (height / 100).toFixed(2);
      ctx.font = fontSize + 'em sans-serif';
      ctx.textBaseline = 'top';
      var text = '160',
        textX = Math.round((width - ctx.measureText(text).width) / 2),
        textY = height / 2;
      ctx.fillText(text, textX, textY);
      ctx.save();
    },
  },
];

export const disease_data = {
  labels: ['Kidney Cancer', 'Mouth Cancer', 'Lorem'],
  datasets: [
    {
      label: 'Total No. Of Patients',
      data: [114, 26, 20],
      backgroundColor: [
        'rgba(243, 115, 36, 0.8)',
        'rgba(134, 158, 166, 0.8)',
        'rgba(0, 0, 0, 0.8)',
      ],
      borderColor: [
        'rgba(243, 115, 36, 1)',
        'rgba(134, 158, 166, 1)',
        'rgba(0, 0, 0, 1)',
      ],
      borderWidth: 2,
    },
  ],
};

const PatientSummary = () => {
  const [values, setValues] = useState([11, 20]);
  const [dimensions, setDimensions] = useState({ width: 150, height: 150 });
  return (
    <Measure
      bounds
      onResize={(contentRect) => {
        setDimensions(contentRect.bounds);
        console.log(dimensions.width / 2);
      }}
    >
      {({ measureRef }) => (
        <div style={{ height: '100%' }} ref={measureRef}>
          <Card containerHeight={true} primaryText="No. of Patients">
            <div className="patient-summary">
              <div className="patient-summary__top">
                <div>
                  <Text>Gender</Text>
                  <Select
                    className="react-select-container"
                    options={[
                      { value: 'male', label: 'Male' },
                      { value: 'female', label: 'Female' },
                      { value: 'unkown', label: 'Unkown' },
                    ]}
                  />
                </div>
                <div>
                  <Text>Cancer Type</Text>
                  <Select
                    className="react-select-container"
                    options={[
                      { value: 'male', label: 'Male' },
                      { value: 'female', label: 'Female' },
                      { value: 'unkown', label: 'Unkown' },
                    ]}
                  />
                </div>
              </div>
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                }}
              >
                <Text>Age&nbsp;&nbsp;&nbsp;</Text>
                <Range
                  step={0.1}
                  min={0}
                  max={100}
                  values={[11, 20]}
                  onChange={() => {}}
                  renderTrack={({ props, children }) => (
                    <div
                      onMouseDown={props.onMouseDown}
                      onTouchStart={props.onTouchStart}
                      style={{
                        ...props.style,
                        height: '36px',
                        display: 'flex',
                        width: '100%',
                      }}
                    >
                      <div
                        ref={props.ref}
                        style={{
                          height: '5px',
                          width: '100%',
                          borderRadius: '4px',
                          background: getTrackBackground({
                            values,
                            colors: ['#ccc', '#F37324', '#ccc'],
                            min: MIN,
                            max: MAX,
                            rtl,
                          }),
                          alignSelf: 'center',
                        }}
                      >
                        {children}
                      </div>
                    </div>
                  )}
                  renderThumb={({ index, props, isDragged }) => (
                    <div
                      {...props}
                      style={{
                        ...props.style,
                        height: '15px',
                        width: '15px',
                        borderRadius: '50%',
                        backgroundColor: '#FFF',
                        display: 'flex',
                        justifyContent: 'center',
                        alignItems: 'center',
                        border: '2px solid #F37324',
                        boxShadow: '0px 2px 6px #AAA',
                      }}
                    >
                      <div
                        style={{
                          position: 'absolute',
                          top: '-28px',
                          color: '#fff',
                          fontWeight: 'bold',
                          fontSize: '14px',
                          fontFamily:
                            'Arial,Helvetica Neue,Helvetica,sans-serif',
                          padding: '4px',
                          borderRadius: '4px',
                          backgroundColor: '#F37324',
                        }}
                      >
                        {values[index].toFixed(1)}
                      </div>
                    </div>
                  )}
                />
              </div>
              <div className="patient-summary__bottom">
                <div className="patient-summary__charts">
                  <div>
                    <Text
                      fontWeight={600}
                      fontSize="1.4rem"
                      textAlign="center"
                      lineHeight={8}
                    >
                      By Gender
                    </Text>
                    <Doughnut
                      data={gender_data}
                      plugins={plugins}
                      options={{
                        maintainAspectRatio: true,
                        responsive: true,
                        plugins: {
                          legend: {
                            display: false,
                          },
                        },
                      }}
                    />
                  </div>
                  <div>
                    <Text
                      fontWeight={600}
                      fontSize="1.4rem"
                      textAlign="center"
                      lineHeight={8}
                    >
                      By Disease
                    </Text>
                    <Doughnut
                      data={disease_data}
                      plugins={plugins}
                      options={{
                        maintainAspectRatio: true,
                        responsive: true,
                        plugins: {
                          legend: {
                            display: false,
                          },
                        },
                      }}
                    />
                  </div>
                </div>
                <div
                  style={{
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'center',
                    alignItems: 'center',
                  }}
                >
                  <Text>By Age</Text>
                  <HighlightedValue>14567</HighlightedValue>
                </div>
              </div>
            </div>
          </Card>
        </div>
      )}
    </Measure>
  );
};

export default PatientSummary;
