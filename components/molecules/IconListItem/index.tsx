import Text from 'components/atoms/Text'
import React from 'react'

interface IconListItemProps {
  label?: string
  value: string
  icon: JSX.Element
  href?: string
}

const IconListItem = ({ icon, value, label = '', href }: IconListItemProps) => {
  const content = (
    <div
      className={`flex flex-row place-content-between place-items-center w-fit ${
        label == '' ? 'space-x-6' : 'space-x-7'
      } ${href ? 'cursor-pointer hover:opacity-80' : ''}`}
    >
      <div
        className={`rounded bg-light ${label == '' ? 'p-2.5' : 'p-5'} ${
          label == '' ? 'text-xl' : 'text-3xl'
        } text-white`}
      >
        {icon}
      </div>
      <div className="space-y-1">
        {label == '' ? '' : <Text textStyle="IconListLabel" value={label} />}
        {label == '' ? (
          <Text textStyle="IconListValueWithoutKey" value={value} />
        ) : (
          <Text textStyle="IconListValue" value={value} />
        )}
      </div>
    </div>
  )

  if (href) {
    return (
      <a href={href} target="_blank" rel="noopener noreferrer">
        {content}
      </a>
    )
  }

  return content
}

export default IconListItem
