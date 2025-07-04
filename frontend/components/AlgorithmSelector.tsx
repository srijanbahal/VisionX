import React, { Fragment } from 'react';
import { Listbox, Transition } from '@headlessui/react';
import { CheckIcon, ChevronUpDownIcon } from '@heroicons/react/20/solid';

const algorithms = [
  { id: 'canny', name: 'Canny Edge Detection' },
  { id: 'log', name: 'Laplacian of Gaussian (LoG)' },
  { id: 'dog', name: 'Difference of Gaussians (DoG)' },
  { id: 'glcm', name: 'Gray-Level Co-occurrence Matrix (GLCM)' },
  { id: 'hough', name: 'Hough Transform' },
  { id: 'chain', name: 'Chain Code' },
  { id: 'histogram', name: 'Histogram Equalization' },
  { id: 'affine', name: 'Affine Transformation' },
  { id: 'region-growing', name: 'Region Growing' },
  { id: 'split-merge', name: 'Splitting & Merging' },
];

interface AlgorithmSelectorProps {
  selectedAlgorithm: string;
  onSelect: (algorithm: string) => void;
}

const AlgorithmSelector = ({ selectedAlgorithm, onSelect }: AlgorithmSelectorProps) => {
  const selected = algorithms.find(a => a.id === selectedAlgorithm) || algorithms[0];

  return (
    <div className="w-full">
      <Listbox value={selectedAlgorithm} onChange={onSelect}>
        <div className="relative mt-1">
          <Listbox.Button className="relative w-full cursor-default rounded-lg bg-white py-2 pl-3 pr-10 text-left border focus:outline-none focus-visible:border-blue-500 focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75 focus-visible:ring-offset-2 focus-visible:ring-offset-blue-300 sm:text-sm">
            <span className="block truncate">{selected.name}</span>
            <span className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
              <ChevronUpDownIcon
                className="h-5 w-5 text-gray-400"
                aria-hidden="true"
              />
            </span>
          </Listbox.Button>
          <Transition
            as={Fragment}
            leave="transition ease-in duration-100"
            leaveFrom="opacity-100"
            leaveTo="opacity-0"
          >
            <Listbox.Options className="absolute mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm z-10">
              {algorithms.map((algorithm) => (
                <Listbox.Option
                  key={algorithm.id}
                  className={({ active }) =>
                    `relative cursor-default select-none py-2 pl-10 pr-4 ${
                      active ? 'bg-blue-100 text-blue-900' : 'text-gray-900'
                    }`
                  }
                  value={algorithm.id}
                >
                  {({ selected }) => (
                    <>
                      <span
                        className={`block truncate ${
                          selected ? 'font-medium' : 'font-normal'
                        }`}
                      >
                        {algorithm.name}
                      </span>
                      {selected ? (
                        <span className="absolute inset-y-0 left-0 flex items-center pl-3 text-blue-600">
                          <CheckIcon className="h-5 w-5" aria-hidden="true" />
                        </span>
                      ) : null}
                    </>
                  )}
                </Listbox.Option>
              ))}
            </Listbox.Options>
          </Transition>
        </div>
      </Listbox>
    </div>
  );
};

export default AlgorithmSelector; 