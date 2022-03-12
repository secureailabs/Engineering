import React, { useEffect, useState } from 'react';

import Text from '@secureailabs/web-ui/components/Text';
import _ from 'lodash';
import Measure from 'react-measure';
import 'chartjs-plugin-labels';

import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  LinearScale,
  BarElement,
  CategoryScale,
} from 'chart.js';
import { Doughnut, Bar } from 'react-chartjs-2';
import { Range, getTrackBackground } from 'react-range';

import HighlightedValue from '@secureailabs/web-ui/components/HighlightedValue';

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement
);

import Card from '@secureailabs/web-ui/components/Card';

import fake_data_json from '@assets/fake_data.json';

import Select from 'react-select';
const STEP = 1;
const MIN = 0;
const MAX = 100;
const rtl = false;

const PatientSummary = ({
  containerHeight = true,
}: {
  containerHeight?: boolean;
}) => {
  const plugins = [
    {
      beforeDraw: function (chart: any) {
        var width = chart.width,
          height = chart.height,
          ctx = chart.ctx;
        ctx.restore();
        var fontSize = (height / 100).toFixed(2);
        ctx.font = fontSize + 'em sans-serif';
        ctx.textBaseline = 'top';
        var text = fake_data.length,
          textX = Math.round((width - ctx.measureText(text).width) / 2),
          textY = height / 2;
        ctx.fillText(text, textX, textY);
        ctx.save();
      },
    },
  ];
  const applyFilters = () => {
    const filtered_by_age = _.filter(fake_data_json, function (o) {
      return age_filter[0] < o.age && age_filter[1] > o.age;
    });
    const filtered_by_cancer_type = cancer_type_filter
      ? _.filter(filtered_by_age, function (o) {
          return o.cancer_type === cancer_type_filter;
        })
      : filtered_by_age;
    const filtered_by_gender = gender_filter
      ? _.filter(filtered_by_cancer_type, function (o) {
          return o.gender === gender_filter;
        })
      : filtered_by_cancer_type;
    const filtered_by_hospital = hospital_filter
      ? _.filter(filtered_by_gender, function (o) {
          return o.hospital === hospital_filter;
        })
      : filtered_by_gender;
    const filtered_by_ethnicity = ethnicity_filter
      ? _.filter(filtered_by_hospital, function (o) {
          return o.ethnicity === ethnicity_filter;
        })
      : filtered_by_hospital;
    setFakeData(filtered_by_ethnicity);
  };

  const [fake_data, setFakeData] = useState(fake_data_json);

  console.log(Object.keys(_.groupBy(fake_data, 'gender')));

  const gender_data = {
    labels: Object.keys(_.groupBy(fake_data, 'gender')),
    datasets: [
      {
        label: 'Total No. Of Patients',
        data: Object.values(_.groupBy(fake_data, 'gender')).map(
          (el) => el.length
        ),
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

  const ethnicity_data = {
    labels: Object.keys(_.groupBy(fake_data, 'ethnicity')),
    datasets: [
      {
        label: 'Total No. Of Patients',
        data: Object.values(_.groupBy(fake_data, 'ethnicity')).map(
          (el) => el.length
        ),
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

  const hospital_data = {
    labels: Object.keys(_.groupBy(fake_data, 'hospital')),
    datasets: [
      {
        label: 'Total No. Of Patients',
        data: Object.values(_.groupBy(fake_data, 'hospital')).map(
          (el) => el.length
        ),
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

  const disease_data = {
    labels: Object.keys(_.groupBy(fake_data, 'cancer_type')),
    datasets: [
      {
        label: 'Total No. Of Patients',
        data: Object.values(_.groupBy(fake_data, 'cancer_type')).map(
          (el) => el.length
        ),
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

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Chart.js Bar Chart',
      },
    },
  };

  const labels = Object.keys(
    _.groupBy(fake_data, function (o) {
      return Math.ceil(o.age / 10) * 10;
    })
  ).map((el) => `${el || 10 - 9} - ${el}`);
  const data = {
    labels,
    datasets: [
      {
        label: 'Age',
        data: Object.values(
          _.groupBy(fake_data, function (o) {
            return Math.ceil(o.age / 10) * 10;
          })
        ).map((el) => el.length),
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
      },
    ],
  };

  const [age_filter, setAgeFilter] = useState([0, 100]);
  const [cancer_type_filter, setCancerTypeFilter] = useState<
    string | undefined
  >(undefined);
  const [gender_filter, setGenderFilter] = useState<string | undefined>(
    undefined
  );
  const [hospital_filter, setHospitalFilter] = useState<string | undefined>(
    undefined
  );
  const [ethnicity_filter, setEthnicityFilter] = useState<string | undefined>(
    undefined
  );
  const [dimensions, setDimensions] = useState({ width: 150, height: 150 });
  useEffect(() => {
    applyFilters();
  }, [
    age_filter,
    cancer_type_filter,
    gender_filter,
    hospital_filter,
    ethnicity_filter,
  ]);

  return (
    <Measure
      bounds
      onResize={(contentRect: any) => {
        setDimensions(contentRect.bounds);
      }}
    >
      {({ measureRef }) => (
        <div
          style={{ height: containerHeight ? '100%' : 'max-content' }}
          ref={measureRef}
        >
          <Card containerHeight={containerHeight} primaryText="No. of Patients">
            <>
              <div className="patient-summary">
                <div className="patient-summary__top">
                  <div>
                    <Text>Gender</Text>
                    <Select
                      isClearable={true}
                      onChange={(el) => {
                        if (el) {
                          setGenderFilter(el.value);
                        } else {
                          setGenderFilter(undefined);
                        }
                      }}
                      className="react-select-container"
                      options={Object.keys(
                        _.groupBy(fake_data_json, 'gender')
                      ).map((el) => {
                        return {
                          value: el,
                          label: el,
                        };
                      })}
                    />
                  </div>
                  <div>
                    <Text>Cancer Type</Text>
                    <Select
                      isClearable={true}
                      className="react-select-container"
                      onChange={(el) => {
                        if (el) {
                          setCancerTypeFilter(el.value);
                        } else {
                          setCancerTypeFilter(undefined);
                        }
                      }}
                      options={Object.keys(
                        _.groupBy(fake_data_json, 'cancer_type')
                      ).map((el) => {
                        return {
                          value: el,
                          label: el,
                        };
                      })}
                    />
                  </div>
                  <div>
                    <Text>Hospital</Text>
                    <Select
                      isClearable={true}
                      onChange={(el) => {
                        if (el) {
                          setHospitalFilter(el.value);
                        } else {
                          setHospitalFilter(undefined);
                        }
                      }}
                      className="react-select-container"
                      options={Object.keys(
                        _.groupBy(fake_data_json, 'hospital')
                      ).map((el) => {
                        return {
                          value: el,
                          label: el,
                        };
                      })}
                    />
                  </div>
                  <div>
                    <Text>Ethnicity/Race</Text>
                    <Select
                      isClearable={true}
                      onChange={(el) => {
                        if (el) {
                          setEthnicityFilter(el.value);
                        } else {
                          setEthnicityFilter(undefined);
                        }
                      }}
                      className="react-select-container"
                      options={Object.keys(
                        _.groupBy(fake_data_json, 'ethnicity')
                      ).map((el) => {
                        return {
                          value: el,
                          label: el,
                        };
                      })}
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
                    step={STEP}
                    min={MIN}
                    max={MAX}
                    values={age_filter}
                    onChange={(el) => {
                      setAgeFilter(el);
                    }}
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
                              values: age_filter,
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
                          {age_filter[index].toFixed(1)}
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
                        //@ts-ignore
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
                        //@ts-ignore
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
                  <div className="patient-summary__charts">
                    <div>
                      <Text
                        fontWeight={600}
                        fontSize="1.4rem"
                        textAlign="center"
                        lineHeight={8}
                      >
                        By Hospital
                      </Text>
                      <Doughnut
                        data={hospital_data}
                        //@ts-ignore
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
                        By Ethnicity/Race
                      </Text>
                      <Doughnut
                        data={ethnicity_data}
                        //@ts-ignore
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
                </div>
              </div>

              <Bar options={options} data={data} />
            </>
          </Card>
        </div>
      )}
    </Measure>
  );
};

export default PatientSummary;
