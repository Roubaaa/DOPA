import ButtonLink from 'components/atoms/Button/ButtonLink'
import LineDivider from 'components/atoms/LineDivider'
import PageSentence from 'components/molecules/PageSentence'
import SectionSentence from 'components/molecules/SectionSentence'
import PageTemplate from 'components/templates/PageTemplate'
import Image from 'next/image'
import React from 'react'
import { FaPython, FaReact } from 'react-icons/fa'
import { SiTypescript, SiTailwindcss, SiNextdotjs } from 'react-icons/si'

const Home = () => {
  return (
    <>
      <PageTemplate title="Home - DOPA">
        {/* Banner Section */}
        <section
          className="flex flex-col gap-10 items-center"
          data-aos="fade-up"
        >
          <div className="w-10/12 md:w-8/12 text-center">
            <PageSentence
              title="Detection of Prohibited Drilling Areas"
              description="Identifying prohibited drilling zones is challenging due to the complexity of interpreting geospatial data, varying land conditions, and regulatory requirements"
            />
          </div>
          <div className="flex flex-col gap-6 sm:flex-row w-full sm:w-fit">
            <ButtonLink value="Detect" href="/service" />
            <ButtonLink
              value="Learn More"
              color="white"
              style="light"
              href="/about"
            />
          </div>
        </section>

        {/* Language Icons */}
        <section className="py-8 grid grid-cols-5 gap-8 place-items-center border-y border-borderLight" data-aos="fade-left">
          <div className="flex flex-col items-center gap-2">
            <FaPython className="text-6xl text-white" />
            <span className="text-white">Python</span>
          </div>
          <div className="flex flex-col items-center gap-2">
            <SiTypescript className="text-6xl text-white" />
            <span className="text-white">TypeScript</span>
          </div>
          <div className="flex flex-col items-center gap-2">
            <FaReact className="text-6xl text-white" />
            <span className="text-white">React</span>
          </div>
          <div className="flex flex-col items-center gap-2">
            <SiTailwindcss className="text-6xl text-white" />
            <span className="text-white">Tailwind CSS</span>
          </div>
          <div className="flex flex-col items-center gap-2">
            <SiNextdotjs className="text-6xl text-white" />
            <span className="text-white">Next.js</span>
          </div>
        </section>

        {/* How We Work */}
        <section className="grid grid-cols-1 gap-6 sm:gap-8 place-items-center lg:grid-cols-2">
          <aside className="w-full h-[400px] relative" data-aos="fade-right">
            <Image
              src={'/images/how-we-work-illustration.svg'}
              alt="Structured plan"
              fill
              style={{ objectFit: 'fill' }}
            />
          </aside>
          <aside
            className="text-center sm:w-10/12 lg:text-left lg:w-full"
            data-aos="fade-left"
          >
            <SectionSentence
              title="Deep Learning model"
              paragraph="U-net Architecture"
              badge="HOW WE WORK"
            />
            <div className="mt-8">
              <ButtonLink
                value="More details"
                href="/how-we-work"
                size="small"
                color="white"
                style="light"
              />
            </div>
          </aside>
        </section>

        {/* Our Teams */}
        <section className="grid grid-cols-1 gap-6 sm:gap-8 place-items-center lg:grid-cols-2">
          <aside className="text-center sm:w-10/12 lg:text-left lg:w-full">
            <div className="space-y-12" data-aos="fade-right">
              <SectionSentence
                title="Team"
                paragraph="Get to know it!"
                badge="OUR TEAM"
              />
              <ButtonLink
                value="See our Team"
                href="/about"
                size="small"
                color="white"
                style="light"
              />
            </div>
          </aside>
          <aside
            className="w-full h-[400px] relative sm:w-8/12 lg:w-full"
            data-aos="fade-left"
          >
            <Image
              src={'/images/team-illustration.svg'}
              alt="Team illustration"
              fill
              style={{ objectFit: 'fill' }}
            />
          </aside>
        </section>

        <LineDivider />

        {/* General Info */}
        <section className="grid place-items-center gap-16">
          <div className="sm:w-10/12 md:w-8/12 lg:w-6/12 2xl:w-5/12 text-center">
            <SectionSentence
              badge="GENERAL INFO"
              title="What are wellpads?"
            />
          </div>
          <div className="w-full grid gap-14">
            <div className="grid grid-cols-1 gap-y-16 sm:grid-cols-2 sm:gap-x-5">
              <div className="basis-full lg:basis-1/2" data-aos="zoom-in-up">
                <div className="space-y-4">
                  <h3 className="text-xl font-semibold text-white">Youtube Video</h3>
                  <a 
                    href="https://www.youtube.com/watch?v=0R9DGWgzpOY"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-400 hover:text-blue-300"
                  >
                    Watch Video
                  </a>
                </div>
              </div>
              <div className="basis-full lg:basis-1/2" data-aos="zoom-in-up">
                <div className="space-y-4">
                  <h3 className="text-xl font-semibold text-white">Article</h3>
                  <a 
                    href="https://equinox-eng.com/wellsite-wellpads/"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-400 hover:text-blue-300"
                  >
                    Read Article
                  </a>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Images Section */}
        <section className="grid place-items-center gap-16">
          <div className="sm:w-10/12 md:w-8/12 lg:w-6/12 2xl:w-5/12 text-center">
            <SectionSentence
              badge="IMAGES"
              title="Want to see some images?"
            />
          </div>
          <div className="w-full grid grid-cols-1 md:grid-cols-2 gap-8 px-4 sm:px-8 md:px-12">
            <div className="group relative overflow-hidden rounded-xl bg-light p-4 transition-all duration-300 hover:scale-[1.02] hover:shadow-xl">
              <div className="relative h-[400px] w-full">
                <Image
                  src="/images/Figure_1.png"
                  alt="Figure 1"
                  fill
                  className="object-contain transition-transform duration-300 group-hover:scale-105"
                />
              </div>
              <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 transition-opacity duration-300 group-hover:opacity-100">
                <div className="absolute bottom-4 left-4 text-white">
                  <h3 className="text-xl font-bold">Figure 1</h3>
                  <p className="text-sm opacity-90">Sample Image 1</p>
                </div>
              </div>
            </div>
            <div className="group relative overflow-hidden rounded-xl bg-light p-4 transition-all duration-300 hover:scale-[1.02] hover:shadow-xl">
              <div className="relative h-[400px] w-full">
                <Image
                  src="/images/Figure_2.png"
                  alt="Figure 2"
                  fill
                  className="object-contain transition-transform duration-300 group-hover:scale-105"
                />
              </div>
              <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 transition-opacity duration-300 group-hover:opacity-100">
                <div className="absolute bottom-4 left-4 text-white">
                  <h3 className="text-xl font-bold">Figure 2</h3>
                  <p className="text-sm opacity-90">Sample Image 2</p>
                </div>
              </div>
            </div>
          </div>
        </section>
      </PageTemplate>
    </>
  )
}

export default Home
