import React from 'react';
import {Composition} from 'remotion';
import {Anatomy, defaultJob} from './Anatomy';
export const Root: React.FC = () => (
  <Composition id="Anatomy" component={Anatomy as any} durationInFrames={720} fps={30} width={1080} height={1920}
    defaultProps={defaultJob as any}
    calculateMetadata={({props}: any) => ({durationInFrames: Math.round((props.duration || 24) * 30)})} />
);
