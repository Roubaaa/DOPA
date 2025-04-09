import NavBrand from 'components/atoms/NavBrand'
import NavLink from 'components/atoms/NavLink'
import Text from 'components/atoms/Text'
import React from 'react'
import { FaGithub, FaLinkedin } from 'react-icons/fa'

const Footer = () => {
  return (
    <>
      <footer className="mt-32 pb-16">
        <div className="flex flex-col gap-8 lg:flex-row lg:gap-16 xl:gap-20">
          <div className="space-y-5">
            <NavBrand />
            <div className="">
              <Text
                value={`Copyright © ${new Date().getFullYear()}`}
                textStyle="SectionParagraph"
              />
              <Text
                value={`Design By DOPA LLC`}
                textStyle="SectionParagraph"
              />
            </div>
          </div>
          <div className="grid grid-cols-3 gap-8 sm:grid-cols-3 lg:gap-16 xl:gap-20">
            <div className="space-y-5">
              <Text value="SOCIAL MEDIA" textStyle="FooterLinkGroupTitle" />
              <div className="space-y-[10px] flex flex-col">
                <a 
                  href="https://github.com/Roubaaa" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="flex items-center gap-2 text-white hover:text-gray-300"
                >
                  <FaGithub size={20} />
                  <span>GitHub</span>
                </a>
                <a 
                  href="https://www.linkedin.com/in/ruba-alsoheil-4173a01ab?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="flex items-center gap-2 text-white hover:text-gray-300"
                >
                  <FaLinkedin size={20} />
                  <span>LinkedIn</span>
                </a>
              </div>
            </div>
            <div className="space-y-5">
              <Text value="DOPA" textStyle="FooterLinkGroupTitle" />
              <div className="space-y-[10px]">
                <NavLink value="About" href="/about" />
                <NavLink value="Contact" href="/contact" />
                <NavLink value="Detect" href="/quote" />
              </div>
            </div>
            <div className="space-y-5">
              <Text value="RESOURCES" textStyle="FooterLinkGroupTitle" />
              <div className="space-y-[10px]">
                <a 
                  href="https://1drv.ms/f/c/774cc792b602f58c/EhsIOD--_rRDhUISOW_uS2YBk02ZGYbITX2jVrkO_GCZZw?e=havyyC" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="block text-white hover:text-gray-300"
                >
                  Data
                </a>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </>
  )
}

export default Footer
