import React, { useEffect, useState } from 'react';

import Text from '@secureailabs/web-ui/components/Text';
import _ from 'lodash';
import Measure from 'react-measure';
import ChartDataLabels from 'chartjs-plugin-datalabels';
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
  BarElement,
  ChartDataLabels
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
   
    },
  ];
  const [fake_data, setFakeData] = useState(fake_data_json);


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

  const race_data = {
    labels: Object.keys(_.groupBy(fake_data, 'race')),
    datasets: [
      {
        label: 'Total No. Of Patients',
        data: Object.values(_.groupBy(fake_data, 'race')).map(
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
  ).map((el) => `${parseInt(el) - 10} - ${parseInt(el)}`);
  const data = {
    labels,
    datasets: [
      {
        label: 'Patient Count',
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
    Array<string>
  >([]);
  const [gender_filter, setGenderFilter] = useState<Array<string>>(
    []
  );
  const [hospital_filter, setHospitalFilter] = useState<Array<string>>(
    []
  );
  const [race_filter, setRaceFilter] = useState<Array<string>>(
    []
  );
  const splitByWordCount = (str: string, count: number): string[] => {
  const arr = str.split(' ')
  const r = [];
  while (arr.length) {
    r.push(arr.splice(0, count).join(' '))
  }
  return r;
}
  const [dimensions, setDimensions] = useState({ width: 150, height: 150 });
  const applyFilters = (): void => {
    const filters = [{
        filter_key: "gender",
        filter: gender_filter,
        filter_function: "equality"
      }, 
      { 
        filter_key: "cancer_type", 
        filter: cancer_type_filter,
        filter_function: "equality" 
      },
      { 
        filter_key: "hospital", 
        filter: hospital_filter,
        filter_function: "equality" 
      },
      { 
        filter_key: "race", 
        filter: race_filter,
        filter_function: "equality" 
      },
      { 
        filter_key: "age", 
        filter: age_filter,
        filter_function: "in-between" 
      }
        ];

    let filtered_data = fake_data_json;
    for(const { filter_key, filter_function, filter} of filters){
          filtered_data = _.filter((filtered_data), function(o){
            if(filter_function === "equality" && filter.length !== 0){
              //@ts-ignore
            return filter.includes(o[filter_key]);
              }  else if (filter_function === "in-between") {

      return filter[0] < o.age && filter[1] > o.age;
                }
 
              return true; 
            })
        }
    setFakeData(filtered_data);
  };


  useEffect(() => {
    applyFilters();
  }, [
    age_filter,
    cancer_type_filter,
    gender_filter,
    hospital_filter,
    race_filter,
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
                    <Text>Hospital</Text>
                    <Select
                      isClearable={true}
                      isMulti={true}
                      onChange={(el) => {
                          setHospitalFilter(el.map((e) => e.value));
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
                    <Text>Gender</Text>
                    <Select
                      isClearable={true}
                      isMulti={true}
                      onChange={(el) => {
                          setGenderFilter(el.map((e) => e.value));
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
                    <Text>Race</Text>
                    <Select
                      isClearable={true}
                      isMulti={true}
                      onChange={(el) => {
                          setRaceFilter(el.map((e) => e.value));
                      }}
                      className="react-select-container"
                      options={Object.keys(
                        _.groupBy(fake_data_json, 'race')
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
                      isMulti={true}
                      className="react-select-container"
                      onChange={(el) => {
                          setCancerTypeFilter(el.map((e) => e.value));
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
                          {age_filter[index].toFixed(0)}
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
                        By Hospital
                      </Text>
                      <Doughnut
                        data={hospital_data}

                      plugins={[ChartDataLabels]}
                        options={{
                          maintainAspectRatio: true,
                          responsive: true,
                          plugins: {
                            legend: {
                              display: false,
                            },
                            tooltip: {
                                callbacks: {
                                    label: function(e){
                                      return splitByWordCount(e.label,2)
                                    }
                                  },
                              }
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
                            tooltip: {
                                callbacks: {
                                    label: function(e){
                                      return splitByWordCount(e.label,2)
                                    }
                                  },
                              }
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
                        By Race
                      </Text>
                      <Doughnut
                        data={race_data}
                        //@ts-ignore
                        plugins={plugins}
                        options={{
                          maintainAspectRatio: true,
                          responsive: true,
                          plugins: {
                            legend: {
                              display: false,
                            },
                             tooltip: {
                                callbacks: {
                                    label: function(e){
                                      return splitByWordCount(e.label,3)
                                    }
                                  },
                              }
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
                       
                        options={{
                          maintainAspectRatio: true,
                          responsive: true,
                          plugins: {
                            legend: {
                              display: false,
                            },
                            tooltip: {
                                callbacks: {
                                    label: function(e){
                                      return e.label
                                    }
                                      
                                  },
                              }
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
