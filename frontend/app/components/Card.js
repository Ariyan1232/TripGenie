import { View, StyleSheet } from 'react-native';
import { Colors } from '../constants/colors';

export default function Card({ children, style, raised = false }) {
  return (
    <View style={[styles.card, raised && styles.raised, style]}>
      {children}
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: Colors.surface,
    borderRadius: 16,
    padding: 16,
    borderWidth: 1,
    borderColor: Colors.border,
    marginBottom: 12,
  },
  raised: {
    backgroundColor: Colors.surfaceRaised,
  },
});