import Image from 'next/image'
import React from 'react'

interface TeamCardProps {
  imageSrc: string
  name: string
  job: string
}

const TeamCard = ({ imageSrc, name, job }: TeamCardProps) => {
  return (
    <div className="w-full max-w-[280px] rounded-2xl bg-[#1A1A1A] overflow-hidden">
      <div className="w-full aspect-square relative">
        <Image
          src={imageSrc}
          layout="fill"
          objectFit="cover"
          alt={name}
        />
      </div>
      <div className="p-6 text-center">
        <h3 className="text-xl font-medium text-white mb-1">{name}</h3>
        <p className="text-[#888888]">{job}</p>
      </div>
    </div>
  )
}

export default TeamCard 