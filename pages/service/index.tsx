import React, { useState } from 'react'
import PageTemplate from 'components/templates/PageTemplate'
import PageSentence from 'components/molecules/PageSentence'
import LineDivider from 'components/atoms/LineDivider'
import Image from 'next/image'
import SectionSentence from 'components/molecules/SectionSentence'
import Button, { ButtonProps } from 'components/atoms/Button'
import {
  FiArrowUp,
  FiCheckCircle,
  FiDownload,
  FiGlobe,
  FiLayout,
  FiMonitor,
  FiRefreshCcw,
  FiSmartphone,
  FiUpload,
  FiImage,
  FiAlertCircle
} from 'react-icons/fi'
import SmallCardIcon from 'components/molecules/Card/SmallCardIcon'
import CardListIcon from 'components/molecules/Card/CardListIcon'
import TextArrowLink from 'components/molecules/TextArrowLink'
import IconListItem from 'components/molecules/IconListItem'
import SelectGroup from 'components/molecules/FormGroup/SelectGroup'

const Services = () => {
  const [selectedModel, setSelectedModel] = useState('wellpad')
  const [imageFile, setImageFile] = useState<File | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [results, setResults] = useState<{
    mask: string;
    overlay: string;
  } | null>(null)

  const handleModelChange = (value: string) => {
    setSelectedModel(value)
    setImageFile(null) // Reset image when model changes
  }

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setImageFile(e.target.files[0])
    }
  }

  const handleDetect = async () => {
    if (!imageFile) {
      setError('Please upload an image first')
      return
    }

    setIsLoading(true)
    setError(null)
    setResults(null)

    try {
      const formData = new FormData()
      formData.append('image', imageFile)

      const response = await fetch('/api/detect', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.details || errorData.error || 'Detection failed')
      }

      const data = await response.json()
      setResults(data)
    } catch (error) {
      console.error('Detection error:', error)
      setError(error instanceof Error ? error.message : 'Failed to process image')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <>
      <PageTemplate title='Detect - DOPA'>
        <section className="grid place-items-center" data-aos="zoom-in-up">
          <div className="text-center sm:w-10/12 md:w-8/12 lg:w-6/12">
            <PageSentence
              badge="DETECT"
              title="Detect prohibited areas"
            />
          </div>
        </section>
        <LineDivider />
        <section className="grid grid-cols-1 gap-6 sm:gap-8 place-items-center lg:grid-cols-2">
          <aside className="w-full h-[400px] relative" data-aos="fade-right">
            <Image
              src="/images/development-illustration.svg"
              alt="Development illustration"
              width={500}
              height={300}
              style={{ objectFit: 'contain' }}
              priority
            />
          </aside>
          <aside
            className="text-center sm:w-10/12 lg:text-left lg:w-full"
            data-aos="fade-left"
          >
            <div className="space-y-12">
              <SectionSentence
                title="Wellpad"
                badge="IMPORTANCE"
              />
              <div className="space-y-8">
                <IconListItem
                  icon={<FiCheckCircle />}
                  label="Efficiency"
                  value="It ensures efficiency and accuracy, regulatory compliance, environmental protection."
                />
                <IconListItem
                  icon={<FiCheckCircle />}
                  label="Essential"
                  value="It is essential for detecting prohibited areas, identifying abandoned wells, and analyzing clustered fields."
                />
                <TextArrowLink href="/how-we-work" label="More info" />
              </div>
            </div>
          </aside>
        </section>
        <LineDivider />
        <section className="grid place-items-center gap-8" data-aos="fade-up">
          <div className="w-full max-w-md space-y-6">
            <div className="text-center">
              <SectionSentence
                title="Select Detection Model"
                badge="MODEL"
              />
              <div className="mt-4 mb-6">
                <a
                  href="https://browser.dataspace.copernicus.eu/?zoom=12&lat=40.42369&lng=-93.92281&themeId=MONITORING&visualizationUrl=U2FsdGVkX18GdFVNLy494qgnKHW731vSpl7Z0h3QVS2Rc1e6v4MDbllDxjht4JQ49qHu0Ol5fwfK5jaZUJwsr6Hiic32T4W7NZWvYAEsLkg3ARpYBWC9cTp2U2MhCe9v&datasetId=S2_L2A_CDAS&fromTime=2025-04-06T00%3A00%3A00.000Z&toTime=2025-04-06T23%3A59%3A59.999Z&layerId=2_FALSE_COLOR&demSource3D=%22MAPZEN%22&cloudCoverage=30&dateMode=SINGLE"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 text-blue-500 hover:text-blue-400 transition-colors"
                >
                  <FiGlobe className="text-xl" />
                  GET SATELLITE IMAGES
                </a>
              </div>
            </div>
            <SelectGroup
              label=""
              options={[
                { label: 'Wellpad Detection', value: 'wellpad' }
              ]}
              defaultValue="wellpad"
            />
            {selectedModel && (
              <div className="space-y-6">
                <div className="relative">
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleImageUpload}
                    className="hidden"
                    id="image-upload"
                  />
                  <label
                    htmlFor="image-upload"
                    className="flex flex-col items-center justify-center gap-2 p-8 border-2 border-dashed border-gray-600 rounded-lg cursor-pointer hover:border-white transition-colors"
                  >
                    <FiUpload className="text-3xl text-gray-400" />
                    <span className="text-gray-400">
                      {imageFile ? imageFile.name : 'Click to upload image'}
                    </span>
                    {imageFile && (
                      <span className="text-sm text-green-500 flex items-center gap-1">
                        <FiCheckCircle /> Image selected
                      </span>
                    )}
                  </label>
                </div>
                <Button
                  value="Detect Wellpads"
                  onClick={handleDetect}
                  style="solid"
                  color="primary"
                  disabled={!imageFile || isLoading}
                />
              </div>
            )}
          </div>
        </section>

        {/* Results Section */}
        {isLoading && (
          <div className="mt-8 text-center space-y-4" data-aos="fade-up">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-gray-200 border-t-blue-500"></div>
            <p className="text-lg text-gray-400">Processing image...</p>
          </div>
        )}

        {error && (
          <div className="mt-8 p-6 bg-red-900/20 border border-red-500/50 rounded-lg text-center" data-aos="fade-up">
            <div className="flex items-center justify-center gap-2 text-red-500">
              <FiAlertCircle className="text-xl" />
              <p className="font-medium">{error}</p>
            </div>
          </div>
        )}

        {results && (
          <section className="mt-12 grid grid-cols-1 md:grid-cols-2 gap-12" data-aos="fade-up">
            <div className="space-y-4">
              <h3 className="text-xl font-semibold text-center text-gray-400">Detection Mask</h3>
              <div className="relative w-full h-80 border border-gray-600 rounded-lg overflow-hidden bg-gray-900/50">
                <Image
                  src={`data:image/png;base64,${results.mask}`}
                  alt="Detection Mask"
                  fill
                  style={{ objectFit: 'contain', padding: '1rem' }}
                />
              </div>
            </div>
            <div className="space-y-4">
              <h3 className="text-xl font-semibold text-center text-gray-400">Overlay</h3>
              <div className="relative w-full h-80 border border-gray-600 rounded-lg overflow-hidden bg-gray-900/50">
                <Image
                  src={`data:image/png;base64,${results.overlay}`}
                  alt="Overlay"
                  fill
                  style={{ objectFit: 'contain', padding: '1rem' }}
                />
              </div>
            </div>
          </section>
        )}
      </PageTemplate>
    </>
  )
}

export default Services
