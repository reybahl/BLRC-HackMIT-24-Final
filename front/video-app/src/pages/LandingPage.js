import React from 'react';
import { Link } from 'react-router-dom';
import styled, { keyframes } from 'styled-components';
import { motion } from 'framer-motion';

// You'll need to replace this with your actual video or high-quality image
const backgroundVideo = 'path/to/your/background-video.mp4';

const fadeIn = keyframes`
  from { opacity: 0; }
  to { opacity: 1; }
`;

const Container = styled.div`
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  color: white;
  position: relative;
  overflow: hidden;
  padding-top: 64px; // Add this line to account for the AppBar height
`;

const VideoBackground = styled.video`
  position: absolute;
  right: 0;
  bottom: 0;
  min-width: 100%;
  min-height: 100%;
  width: auto;
  height: auto;
  z-index: -1;
  object-fit: cover;
`;

const Overlay = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(76, 0, 255, 0.6) 0%, rgba(0, 225, 255, 0.6) 100%);
`;

const Content = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  text-align: center;
  z-index: 1;
`;

const Title = styled(motion.h1)`
  font-size: 4rem;
  margin-bottom: 1rem;
  animation: ${fadeIn} 1s ease-out;
`;

const Subtitle = styled(motion.h2)`
  font-size: 1.5rem;
  margin-bottom: 2rem;
  max-width: 600px;
  animation: ${fadeIn} 1s ease-out 0.5s forwards;
  opacity: 0;
`;

const CTAButton = styled(motion.button)`
  padding: 1rem 2rem;
  font-size: 1.2rem;
  background: rgba(255, 255, 255, 0.2);
  border: 2px solid white;
  color: white;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);

  &:hover {
    background: white;
    color: #4c00ff;
  }
`;

const FeatureSection = styled.div`
  display: flex;
  justify-content: space-around;
  margin-top: 4rem;
`;

const FeatureCard = styled(motion.div)`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 2rem;
  width: 250px;
  text-align: center;
`;

const FeatureIcon = styled.div`
  font-size: 3rem;
  margin-bottom: 1rem;
`;

const FeatureTitle = styled.h3`
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
`;

const FeatureDescription = styled.p`
  font-size: 0.9rem;
`;

const LandingPage = () => {
  return (
    <Container>
      <VideoBackground autoPlay loop muted>
        <source src={backgroundVideo} type="video/mp4" />
      </VideoBackground>
      <Overlay />
      <Content>
        <Title
          initial={{ y: -50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
          Revolutionize Your Learning
        </Title>
        <Subtitle
          initial={{ y: 50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          Dive into an immersive world of interactive video learning. Unlock your potential and gain deep understanding.
        </Subtitle>
        <CTAButton
          as={Link}
          to="/upload"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          Start Your Journey
        </CTAButton>

        <FeatureSection>
          {[
            { icon: '🌍', title: 'Language Mastery', description: 'Immerse yourself in new languages' },
            { icon: '🎬', title: 'Film Analysis', description: 'Dive deep into cinematic worlds' },
            { icon: '📚', title: 'Interactive Learning', description: 'Engage with educational content' },
          ].map((feature, index) => (
            <FeatureCard
              key={index}
              initial={{ y: 50, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ duration: 0.5, delay: 0.4 + index * 0.1 }}
            >
              <FeatureIcon>{feature.icon}</FeatureIcon>
              <FeatureTitle>{feature.title}</FeatureTitle>
              <FeatureDescription>{feature.description}</FeatureDescription>
            </FeatureCard>
          ))}
        </FeatureSection>
      </Content>
    </Container>
  );
};

export default LandingPage;
