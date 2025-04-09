import PageSentence from 'components/molecules/PageSentence'
import SectionSentence from 'components/molecules/SectionSentence'
import TeamCard from 'components/organisms/TeamCard'
import PageTemplate from 'components/templates/PageTemplate'
import Image from 'next/image'
import React from 'react'
import { FaPython, FaReact } from 'react-icons/fa'
import { SiTypescript, SiTailwindcss, SiNextdotjs } from 'react-icons/si'

const About = () => {
  return (
    <PageTemplate title="About - DOPA">
      <section className="grid grid-cols-1 lg:grid-cols-2 gap-8 place-items-center">
        <aside className="w-full" data-aos="fade-down-right">
          <div className="w-full h-[400px] relative">
            <Image
              src={'/images/about-illustration.webp'}
              layout="fill"
              objectFit="contain"
              alt="3D Illustration"
            />
          </div>
        </aside>
        <aside
          className="sm:w-10/12 md:w-8/12 lg:w-full text-center lg:text-left"
          data-aos="fade-down-left"
        >
          <SectionSentence
            badge="ABOUT"
            title="Ruba Alsoheil"
          />
          <p className="mt-4 text-gray-400">
            Petroleum Engineer | M.Sc. in Chemical Engineering
          </p>
        </aside>
      </section>
      <section className="grid place-items-center gap-16">
        <div
          className="sm:w-10/12 md:w-8/12 lg:w-6/12 2xl:w-5/12 text-center"
          data-aos="zoom-in-up"
        >
          <SectionSentence
            badge="LANGUAGES"
            title="Languages used in this project"
          />
        </div>
        <div className="w-full grid gap-14">
          <div data-aos="fade-right" className="grid grid-cols-5 gap-8 place-items-center">
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
          </div>
        </div>
      </section>
      <section className="grid place-items-center gap-16">
        <div className="w-full grid place-items-center">
          <div data-aos="fade-up">
            <TeamCard
              imageSrc="/images/ruba.jpg"
              job="Petroleum Engineer"
              name="Ruba Alsoheil"
            />
          </div>
        </div>
      </section>
    </PageTemplate>
  )
}

export default About
