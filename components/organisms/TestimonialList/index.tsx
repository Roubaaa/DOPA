import React from 'react'
import { Swiper, SwiperSlide } from 'swiper/react'
import 'swiper/css'
import 'swiper/css/pagination'
import { Pagination } from 'swiper'
import Image from 'next/image'

const TestimonialList = () => {
  return (
    <div className="w-full">
      <Swiper
        breakpoints={{
          300: {
            spaceBetween: 10,
          },
          640: {
            spaceBetween: 20,
          },
          768: {
            spaceBetween: 40,
          },
          1024: {
            spaceBetween: 50,
          },
        }}
        loop={true}
        pagination={{
          clickable: true,
          type: 'bullets',
          clickableClass: 'swiper-pagination',
          bulletClass: 'swiper-pagination-bullet',
          bulletActiveClass: 'swiper-pagination-bullet-active',
        }}
        direction="horizontal"
        modules={[Pagination]}
        slideClass='swiper-slide'
        slideActiveClass='swiper-slide-active'
      >
        <SwiperSlide className='mt-10'>
          <div className="w-full px-10 py-14 bg-light rounded-md select-none">
            <div className="space-y-5 flex flex-col items-center text-center">
              <div className="relative w-full h-[400px]">
                <Image
                  src="/images/figure_1.png"
                  alt="Figure 1"
                  fill
                  style={{ objectFit: 'contain' }}
                />
              </div>
            </div>
          </div>
        </SwiperSlide>
        <SwiperSlide className='mt-10'>
          <div className="w-full px-10 py-14 bg-light rounded-md select-none">
            <div className="space-y-5 flex flex-col items-center text-center">
              <div className="relative w-full h-[400px]">
                <Image
                  src="/images/figure_2.png"
                  alt="Figure 2"
                  fill
                  style={{ objectFit: 'contain' }}
                />
              </div>
            </div>
          </div>
        </SwiperSlide>
      </Swiper>
    </div>
  )
}

export default TestimonialList
